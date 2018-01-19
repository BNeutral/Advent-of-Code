#[allow(dead_code)]
pub fn advent17_1(input : &str) -> u32  {
    simulate(input)
}

#[allow(dead_code)]
pub fn advent17_2(input : &str) -> u32  {
    solve_for_0(input)
}

const ITERATIONS_1 : u32 = 2017;
const ITERATIONS_2 : u32 = 50000000;

/// Given an input of a step size as a number, solves part 1 of the problem
fn simulate(input : & str) -> u32 {
    let step : usize = input.parse::<usize>().unwrap();
    let mut buffer : Vec<u32> = vec![0];
    let mut current_pos = 0;
    for x in 1..ITERATIONS_1+1 {
        current_pos = (current_pos+step) % buffer.len() + 1;
        buffer.insert(current_pos, x);
    }
    println!("{:?}",buffer);
    buffer[(current_pos+1)%buffer.len()]
}

/// Solves by just checking what would be added in front of 0
fn solve_for_0(input : & str) -> u32 {
    let step : usize = input.parse::<usize>().unwrap();
    let mut len = 1;
    let mut current_pos = 0;
    let mut val_after_0 = 0;
    for x in 1..ITERATIONS_2+1 {
        current_pos = (current_pos+step) % len + 1;
        if current_pos == 1 { val_after_0 = x }
        len += 1;
    }
    val_after_0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test1_1() {
        assert_eq!(638,advent17_1("3"));
    }


}