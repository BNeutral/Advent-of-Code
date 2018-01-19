/// Solution sort of copied from problem 18_1 for productivity, probably should share/refactor some code
use std::collections::HashMap;
use std::thread;
use std::sync::{Arc, Mutex};
use std::sync::mpsc;

const NUMBER_OF_THREADS : i32 = 2;

#[allow(dead_code)]
pub fn advent18_2(input : &str) -> i64 {
    let (instructions, register_count, p_index) = parse_to_instructions(input);
    let instructions0 = Arc::new(instructions);
    let instructions1 = Arc::clone(&instructions0);
    let (sender0, receiver0) = mpsc::channel::<i64>();
    let (sender1, receiver1) = mpsc::channel::<i64>();
    let deadlock_chequer : Arc<Mutex<i32>> = Arc::new(Mutex::new(0));
    let mut context0 = Context::new(register_count,
                                    sender0, receiver1, deadlock_chequer.clone());
    let mut context1 = Context::new(register_count,
                                    sender1, receiver0, deadlock_chequer.clone());
    context0.registers[p_index] = 0;
    context1.registers[p_index] = 1;
    thread::spawn( move || { execute_program(&instructions0, &mut context0) } );
    let thread1 = thread::spawn( move || { execute_program(&instructions1, &mut context1) } );
    thread1.join().unwrap()
}

/// Hashmap wrapper that assigns and returns register indexes for a given register name
struct RegisterTranslator<'a> {
    register_names: HashMap<&'a str, usize>,
    count : usize,
}

impl<'a> RegisterTranslator<'a> {
    fn new() -> RegisterTranslator<'a> {
        RegisterTranslator {
            register_names: HashMap::new(),
            count : 0
        }
    }

    /// Returns the register id for a given register name
    fn get(&mut self, register_name : &'a str) -> usize {
        if self.register_names.contains_key(register_name) {
            *self.register_names.get(register_name).unwrap()
        }
            else {
                self.register_names.insert(register_name,self.count);
                self.count += 1;
                self.count - 1
            }
    }

    /// Returns the number of registers
    fn count(&self) -> usize {
        self.register_names.iter().count()
    }
}

/// Context for instruction execution
struct Context {
    registers : Vec<i64>,
    program_counter : i64,
    amount_sent : i64,
    stop : bool,
    sender : mpsc::Sender<i64>,
    receiver : mpsc::Receiver<i64>,
    deadlock_chequer : Arc<Mutex<i32>>,
}

impl Context {
    fn new(amount_of_registers : usize, sender :  mpsc::Sender<i64>,
           receiver :  mpsc::Receiver<i64>, deadlock_chequer : Arc<Mutex<i32>>) -> Context {
        Context {
            registers : vec![0; amount_of_registers],
            program_counter : 0,
            amount_sent : 0,
            stop : false,
            sender,
            receiver,
            deadlock_chequer,
        }
    }
}

/// Can be a register number or an integer
enum Operand {
    RegisterNumber(usize),
    Immediate(i64),
    None,
}

impl Operand {
    /// Returns a reference to the register needed
    fn get_ref<'a>(&self, context : &'a mut Context) -> &'a mut i64 {
        match *self {
            Operand::RegisterNumber(x) => &mut context.registers[x],
            _ => panic!("Operation parameter missmatch"),
        }
    }

    /// Returns a value
    fn get_val(&self, context : &Context) -> i64 {
        match *self {
            Operand::RegisterNumber(x) => context.registers[x],
            Operand::Immediate(x) => x,
            Operand::None => panic!("Operation parameter missmatch"),
        }
    }
}

/// Struct that represents a instruction to execute if a comparison is successful
/// Note that the return value is to be added to the program_counter
struct Instruction {
    operand1: Operand,
    operand2: Operand,
    operation : fn(&Instruction, &mut Context) -> i64,
}

impl Instruction {
    fn new(operation : &str, operand1 : Operand, operand2 : Operand) -> Instruction {
        Instruction {
            operand1, operand2,
            operation :
            match operation {
                "snd" => Instruction::snd,
                "set" => Instruction::set,
                "add" => Instruction::add,
                "mul" => Instruction::mul,
                "mod" => Instruction::modd,
                "rcv" => Instruction::rcv,
                "jgz" => Instruction::jgz,
                _ => panic!("Unsupported operation"),
            },
        }
    }

    fn snd(&self, context : &mut Context) -> i64 {
        {
            *context.deadlock_chequer.lock().unwrap() += 1;
        }
        match context.sender.send(self.operand1.get_val(context) ) {
            Err(_) => {
                context.stop = true;
                return 1
            }
            _ => {},
        }
        context.amount_sent += 1;
        1
    }

    fn rcv(&self, context : &mut Context) -> i64 {
        self.check_deadlock(context);
        if context.stop { return 1 }
        match context.receiver.recv() {
            Ok(x) => *self.operand1.get_ref(context) = x,
            Err(_) => {
                self.check_deadlock(context);
                return 0;
            },
        }
        1
    }

    fn check_deadlock(&self, context : &mut Context) {
        let mut count = context.deadlock_chequer.lock().unwrap();
        *count -= 1;
        if *count <= -NUMBER_OF_THREADS { // Deadlock
            context.stop = true;
        }
    }

    fn set(&self, context : &mut Context) -> i64 {
        *self.operand1.get_ref(context) = self.operand2.get_val(context);
        1
    }

    fn add(&self, context : &mut Context) -> i64 {
        *self.operand1.get_ref(context) += self.operand2.get_val(context);
        1
    }

    fn mul(&self, context : &mut Context) -> i64 {
        *self.operand1.get_ref(context) *= self.operand2.get_val(context);
        1
    }

    fn modd(&self, context : &mut Context) -> i64 {
        *self.operand1.get_ref(context) %= self.operand2.get_val(context);
        1
    }

    fn jgz(&self, context : &mut Context) -> i64 {
        if self.operand1.get_val(context) > 0 {
            self.operand2.get_val(context)
        }
        else {
            1
        }
    }

    fn execute(&self,  context : &mut Context) -> i64 {
        (self.operation)(self,context)
    }

}

/// Given some properly formatted input, returns a vector of executable instructions and the amoount of registers
/// The input should be of the form "<op> <register> <register or immediate>"
fn parse_to_instructions(input : &str) -> (Vec<Instruction>, usize, usize) {
    let mut translation_table = RegisterTranslator::new();
    let mut instructions : Vec<Instruction> = Vec::new();
    for line in input.lines() {
        let split : Vec<&str> = line.trim().split_whitespace().collect();
        let operation : &str = split[0];
        let operand1 : Operand = {
            match split[1].parse::<i64>() {
                Ok(val) => Operand::Immediate(val),
                Err(_) => Operand::RegisterNumber(translation_table.get(split[1])),
            }
        };
        let operand2 : Operand = {
            if split.len() < 3 { Operand::None }
            else {
                let s = split[2];
                match s.parse::<i64>() {
                    Ok(val) => Operand::Immediate(val),
                    Err(_) => Operand::RegisterNumber(translation_table.get(s)),
                }
            }
        };
        let instruction = Instruction::new(operation, operand1, operand2);
        instructions.push(instruction);
    }
    (instructions, translation_table.count(), translation_table.get("p"))
}

/// Executes the program until... ?
fn execute_program(instructions : &Vec<Instruction>, context : &mut Context ) -> i64 {
    while !context.stop {
        context.program_counter += instructions[context.program_counter as usize].execute(context);
    }
    context.amount_sent
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test2_1() {
        let str = "snd 1\nsnd 2\nsnd p\nrcv a\nrcv b\nrcv c\nrcv d";
        assert_eq!(3,advent18_2(str));
    }

}