/// Solution pointlessly optimized from expecting instructions to repeat on part 2, wasn't the case
use std::collections::HashMap;

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

/// Struct that represents an executable condition composed of a register number, an operation, and a value to compare against
struct Conditional {
    register_number: usize,
    value : i32,
    condition : fn(&Conditional, i32) -> bool,
}

impl Conditional {
    fn new(register_number : usize, condition : &str, value : i32) -> Conditional {
        Conditional {
            register_number,
            value,
            condition :
                match condition {
                    "<" => Conditional::l,
                    ">" => Conditional::g,
                    "<=" => Conditional::le,
                    ">=" => Conditional::ge,
                    "==" => Conditional::e,
                    "!=" => Conditional::ne,
                    _ => panic!("Unsupported comparison"),
                }
        }
    }

    /// Applies the comparison
    fn compare(&self, registers : &Vec<i32>) -> bool {
        (self.condition)(&self, registers[self.register_number])
    }

    fn l(&self, register_value : i32) -> bool {
        register_value < self.value
    }

    fn le(&self, register_value : i32) -> bool {
        register_value <= self.value
    }

    fn g(&self, register_value : i32) -> bool {
        register_value > self.value
    }

    fn ge(&self, register_value : i32) -> bool {
        register_value >= self.value
    }

    fn e(&self, register_value : i32) -> bool {
        register_value == self.value
    }

    fn ne(&self, register_value : i32) -> bool {
        register_value != self.value
    }


}

/// Struct that represents a instruction to execute if a comparison is successful
struct Instruction {
    register_number: usize,
    value : i32,
    operation : fn(&Instruction, &mut i32),
    condition : Conditional,
}

impl Instruction {
    fn new(op_register : usize, op : &str, op_val : i32, cmp_register : usize, cmp : &str, cmp_val : i32) -> Instruction {
        Instruction {
            register_number: op_register,
            value : op_val,
            operation :
            match op {
                "inc" => Instruction::add,
                "dec" => Instruction::sub,
                _ => panic!("Unsupported operation"),
            },
            condition : Conditional::new(cmp_register, cmp, cmp_val),
        }

    }

    fn add(&self, register_value : &mut i32) {
        *register_value += self.value;
    }

    fn sub(&self, register_value : &mut i32) {
        *register_value -= self.value;
    }

    fn execute(&self, registers : &mut Vec<i32>) {
        if self.condition.compare(registers) {
            (self.operation)(&self, &mut registers[self.register_number]);
        }
    }

}

/// Given some properly formatted input, returns a vector of executable instructions
/// Also initializes the register table
/// The input should be of the form "<register_op> <op> <i32> if <register_cmp> <cmp> <i32>"
fn parse_to_instructions(input : &str, registers : &mut Vec<i32>) -> Vec<Instruction> {
    let mut translation_table = RegisterTranslator::new();
    let mut result : Vec<Instruction> = Vec::new();
    for line in input.lines() {
        let split : Vec<&str> = line.split_whitespace().collect();
        let op_register : usize = translation_table.get(split[0]);
        let op : &str = split[1];
        let op_val : i32 = split[2].parse::<i32>().unwrap();
        let cmp_register : usize = translation_table.get(split[4]);
        let cmp : &str = split[5];
        let cmp_val : i32 = split[6].parse::<i32>().unwrap();
        let instruction = Instruction::new(op_register, op, op_val, cmp_register, cmp, cmp_val);
        result.push(instruction);
    }
    for _ in 0..translation_table.count() {
        registers.push(0);
    }
    result
}

#[allow(dead_code)]
pub fn advent8_1(input : &str) -> i32 {
    let mut registers : Vec<i32> = Vec::new();
    let instructions = parse_to_instructions(input, &mut registers);
    for i in instructions {
        i.execute(&mut registers);
    }
    *registers.iter().max().unwrap()
}

#[allow(dead_code)]
pub fn advent8_2(input : &str) -> i32 {
    let mut registers : Vec<i32> = Vec::new();
    let instructions = parse_to_instructions(input, &mut registers);
    let mut max = 0;
    for i in instructions {
        i.execute(&mut registers);
        let val = registers[i.register_number];
        if val > max {
            max = val;
        }
    }
    max
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test1() {
        let str = "b inc 5 if a > 1\na inc 1 if b < 5\nc dec -10 if a >= 1\nc inc -20 if c == 10";
        assert_eq!(1,advent8_1(str));
    }

    #[test]
    fn test2() {
        let str = "b inc 5 if a > 1\na inc 1 if b < 5\nc dec -10 if a >= 1\nc inc -20 if c == 10";
        assert_eq!(10,advent8_2(str));
    }

}
