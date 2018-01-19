#[allow(dead_code)]
pub fn advent13_1(input : &str) -> u32 {
    let mut scanners = parse_input(input);
    simulate(&mut scanners, 0, false)
}

/// TODO: Optimize mathematically solving the set of equations instead of simulating
#[allow(dead_code)]
pub fn advent13_2(input : &str) -> u32 {
    let mut scanners = parse_input(input);
    let mut delay = 0;
    while simulate(&mut scanners, delay, true) > 0 {
        delay += 1;
        for scanner in scanners.iter_mut() {
            scanner.reset();
        }
    }
    delay
}

/// Simulates the scanners, with some small optimizations although there is probably better ones
/// delay sets the starting delay before the simulation begins
/// return_if_caught makes the function return 1 if the packet is caught
fn simulate(scanners : &mut Vec<Scanner>, delay : u32, return_if_caught : bool) -> u32 {
    let mut severity = 0;
    // Note, time is equivalent to the current layer being visited
    for scanner in scanners.iter_mut() {
        let time = scanner.depth as u32 + delay;
        scanner.multiple_step(time);
        if scanner.at_top() {
            severity += scanner.severity();
            if return_if_caught { return 1 }
        }
    }
    severity
}

/// Parses the input and returns a vector of scanners
/// It is assumed the input comes ordered by depth and there's less than 255 layers
fn parse_input(input : &str) -> Vec<Scanner> {
    let mut scanners : Vec<Scanner> = Vec::new();
    for line in input.lines() {
        let line = line.replace(" ","");
        let mut iterator = line.split(":");
        let depth = iterator.next().unwrap().parse::<u8>().unwrap();
        let range =  iterator.next().unwrap().parse::<u8>().unwrap();
        let scanner = Scanner::new(depth, range);
        scanners.push(scanner);
    }
    scanners
}

/// Struct that represents a scanner to simulate
struct Scanner {
    depth : u8,
    pos : u8,
    range_minus_one : u8,
    step_function: fn(&mut Scanner),
}

impl Scanner {
    fn new(depth : u8, range : u8) -> Scanner {
        Scanner { depth, range_minus_one : range - 1, pos : 0, step_function: Scanner::step_forward }
    }

    /// Returns the severity of getting caught by the scanner
    fn severity(&self) -> u32 {
        self.depth as u32 * (self.range_minus_one as u32 + 1)
    }

    /// Moves the scanner once
    fn single_step(&mut self) {
        (self.step_function)(self)
    }

    /// Moves the Scanner multiple times, in a somewhat optimized way
    fn multiple_step(&mut self, steps : u32) {
        let actual_steps = steps % (self.range_minus_one as u32 * 2);
        for _ in 0..actual_steps {
            self.single_step();
        }
    }

    /// Function for stepping forward, checks if it should start stepping backwards instead
    fn step_forward(&mut self) {
        if self.pos == self.range_minus_one {
            self.step_function = Scanner::step_backwards;
            self.single_step()
        }
        self.pos += 1;
    }

    /// Function for stepping backwards, checks if it should start stepping forward instead
    fn step_backwards(&mut self) {
        if self.pos == 0 {
            self.step_function = Scanner::step_forward;
            self.single_step()
        }
        self.pos -=1;
    }

    /// Returns true if the scanner is at the top
    fn at_top(&self) -> bool {
        self.pos == 0
    }

    /// Resets to the starting position
    fn reset(&mut self) {
        self.pos = 0;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test1_1() {
        assert_eq!(24, advent13_1("0: 3\n1: 2\n4: 4\n6: 4"));
    }

    #[test]
    fn test1_2() {
        assert_eq!(10, advent13_2("0: 3\n1: 2\n4: 4\n6: 4"));
    }


}