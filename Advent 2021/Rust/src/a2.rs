use regex::Regex;

#[allow(dead_code)]
pub fn day2(input : &String) -> () {
	println!("Part1: {}", day2_1(&input));
	println!("Part2: {}", day2_2(&input));
}


#[allow(dead_code)]
pub fn day2_1(input : &String) -> i64 {
	let mut pos = 0;
	let mut depth = 0; 

	let reg = Regex::new(r"(\w+) (\d+)").unwrap();
	for line in input.lines(){
		let captures = reg.captures(line).unwrap();
		let command = captures.get(1).unwrap().as_str();
		let value : i64 = captures.get(2).unwrap().as_str().parse().unwrap();
		match command {
			"forward" => pos += value,
			"up" => depth -= value,
			"down" => depth += value,
			_ => {},
		}		
	}

	pos * depth
}

#[allow(dead_code)]
pub fn day2_2(input : &String) -> i64 {
	let mut pos = 0;
	let mut depth = 0; 
	let mut aim = 0;

	let reg = Regex::new(r"(\w+) (\d+)").unwrap();
	for line in input.lines(){
		let captures = reg.captures(line).unwrap();
		let command = captures.get(1).unwrap().as_str();
		let value : i64 = captures.get(2).unwrap().as_str().parse().unwrap();
		match command {
			"forward" => {pos += value;
				depth += aim * value},
			"up" => aim -= value,
			"down" => aim += value,
			_ => {},
		}		
	}

	pos * depth
}


#[cfg(test)]
mod tests {
	use super::*;

	#[test]
	fn test2_1() {
		let input = &String::from("forward 5\ndown 5\nforward 8\nup 3\ndown 8\nforward 2");
		assert_eq!(150,day2_1(&input));
	}

	
	#[test]
	fn test2_2() {
		let input = &String::from("forward 5\ndown 5\nforward 8\nup 3\ndown 8\nforward 2");
		assert_eq!(900,day2_2(&input));
	}	
}
