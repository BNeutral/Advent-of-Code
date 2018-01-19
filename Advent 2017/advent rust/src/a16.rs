#[allow(dead_code)]
pub fn advent16_1(input : &str) -> String  {
    solve(input, 1)
}

#[allow(dead_code)]
pub fn advent16_2(input : &str) -> String  {
    solve(input, 1000000000)
}

/// Solves the problem and returns the corresponding string
fn solve(input : & str, iterations : usize) -> String {
    let mut programs = gen_list(16);
    let starting_programs = programs.clone();
    let mut dance_counter = 0;
    let instructions = parse_input(input);
    for _ in 0..iterations {
        dance(&instructions, &mut programs);
        dance_counter += 1;
        if programs == starting_programs { // A loop has been found, we are again at the start
            break;
        }
    }
    for _ in 0..iterations%dance_counter { // Simply iterate on what we would have removing loops
        dance(&instructions, &mut programs);
    }
    programs.iter().collect::<String>()
}

/// Expects properly formated input of comma separated commands
fn parse_input(input : &str) -> Vec<&str> {
    input.trim().split(",").collect()
}

/// Makes the programs dance
/// Valid commands are:
/// sX
/// xA/B
/// pA/B
fn dance (instructions : &Vec<&str>, programs : &mut Vec<char>) {
    for op in instructions {
        let len = op.len();
        match op[0..1].as_ref() {
            "s" => spin(op[1..len].as_ref(), programs),
            "x" => exchange(op[1..len].as_ref(), programs),
            "p" => partner(op[1..len].as_ref(), programs),
            _ => {},
        }
    }
}

/// Executes the spin instruction on the vector
fn spin(input : &str, programs : &mut Vec<char>) {
    let num = input.parse::<usize>().unwrap();
    for _ in 0..num {
        let first = programs.pop().unwrap();
        programs.insert(0,first);
    }
}

/// Executes the exchange instruction on the vector
fn exchange(input : &str, programs : &mut Vec<char>) {
    let positions = input.split("/").map(|x : &str| -> usize { x.parse::<usize>().unwrap() }).collect::<Vec<usize>>();
    programs.swap(positions[0],positions[1]);
}

/// Executes the partner instruction on the vector
fn partner(input : &str, programs : &mut Vec<char>) {
    let chars : Vec<char> = input.chars().collect();
    let first : char = chars[0];
    let second : char = chars[2];
    let index1 : usize = programs.iter().position(|x : &char| *x == first).unwrap();
    let index2 : usize = programs.iter().position(|x : &char| *x == second).unwrap();
    programs.swap(index1,index2);
}

/// Creates a vector of chars that goes from ASCII a(97) to a(97)+size
fn gen_list(size : u8) -> Vec<char> {
    (97u8..97u8+size).map(|x : u8| -> char { x as char } ).collect::<Vec<char>>()
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test1_1() {
        let mut programs = gen_list(5);
        let instructions = parse_input("s1,x3/4,pe/b");
        dance(&instructions, &mut programs);
        assert_eq!(vec!['b','a','e','d','c'], programs);
    }

    #[test]
    fn test2_1() {
        let mut programs = gen_list(5);
        let instructions = parse_input("s1,x3/4,pe/b");
        dance(&instructions, &mut programs);
        dance(&instructions, &mut programs);
        assert_eq!(vec!['c','e','a','d','b'], programs);
    }

}