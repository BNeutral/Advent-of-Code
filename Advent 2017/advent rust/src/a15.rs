#[allow(dead_code)]
pub fn advent15_1(input : &str) -> u32 {
    let mut generators = parse_input(input, false);
    judge(&mut generators, 40000000)
}

#[allow(dead_code)]
pub fn advent15_2(input : &str) -> u32 {
    let mut generators = parse_input(input, true);
    judge(&mut generators, 5000000)
}

/// We asume the input is a bunch of words, then a space, then a seed, one per line, only 2 lines
fn parse_input(input : &str, second_part : bool) -> (Generator,Generator) {
    let lines : Vec<&str> = input.lines().collect();
    let seed1 = lines[0].split_whitespace().last().unwrap().parse::<u64>().unwrap();
    let seed2 = lines[1].split_whitespace().last().unwrap().parse::<u64>().unwrap();
    let divisibility1 : u64 = { if second_part { 4 } else { 1 } };
    let divisibility2 : u64 = { if second_part { 8 } else { 1 } };
    (Generator::new(16807,seed1, divisibility1),
     Generator::new(48271,seed2, divisibility2))
}

/// Compares the lowest 16 bits of the generators for the amount of iterations
fn judge(generators : &mut (Generator,Generator), iterations : u64 ) -> u32 {
    let mut matches = 0;
    for _ in 0..iterations {
        if generators.0.next_value_lowest_16() == generators.1.next_value_lowest_16() {
            matches += 1;
        }
    }
    matches
}

const REMAINDER_VALUE: u64 = 2147483647;

/// A number generator as defined by the problem
struct Generator {
    factor : u64,
    previous_value : u64,
    divisibility : u64,
}

impl Generator {
    fn new(factor : u64, seed : u64, divisibility : u64) -> Generator {
        Generator { factor, previous_value : seed, divisibility }
    }

    /// Calculates the next value and returns it
    fn next_value(&mut self) -> u64 {
        loop {
            self.previous_value = ( self.previous_value * self.factor) % REMAINDER_VALUE;
            if self.previous_value % self.divisibility == 0 { break; }
        }
        self.previous_value
    }

    /// Calculates the next value but returns only the 16 lowest bits
    fn next_value_lowest_16(&mut self) -> u64 {
        self.next_value() & 0xffff
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test1_1() {
        let mut generators = parse_input("65\n8921\n", false);
        assert_eq!(1, judge(&mut generators, 5));
    }

    #[test]
    fn test1_2() {
        assert_eq!(588, advent15_1("65\n8921\n"));
    }

    #[test]
    fn test2_1() {
        assert_eq!(309, advent15_2("65\n8921\n"));
    }

}