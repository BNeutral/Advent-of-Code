/// Solution sort of copied from problem 8, probably should share some code
use std::collections::HashMap;

#[allow(dead_code)]
pub fn advent18_1(input : &str) -> i64 {
    let (instructions, register_count) = parse_to_instructions(input);
    let mut context = Context::new(register_count);
    execute_program(&instructions, &mut context);
    context.last_rec_freq
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
    last_rec_freq: i64,
    recover : bool,
}

impl Context {
    fn new(amount_of_registers : usize) -> Context {
        Context {
            registers : vec![0; amount_of_registers],
            program_counter : 0,
            last_rec_freq: 0,
            recover : false,
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
        context.last_rec_freq = self.operand1.get_val(context);
        1
    }

    fn rcv(&self, context : &mut Context) -> i64 {
        if  self.operand1.get_val(context) != 0 {
            context.recover = true;
        }
        1
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
fn parse_to_instructions(input : &str) -> (Vec<Instruction>, usize) {
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
    (instructions, translation_table.count())
}

/// Executes the program until a rcv instruction triggers
fn execute_program(instructions : &Vec<Instruction>, context : &mut Context) {
    while !context.recover {
        context.program_counter += instructions[context.program_counter as usize].execute(context);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test1_1() {
        let str = "set a 1\nadd a 2\nmul a a\nmod a 5\nsnd a\nset a 0\nrcv a\njgz a -1\nset a 1\njgz a -2";
        assert_eq!(4,advent18_1(str));
    }

}