/// Given a string, calculates the sum of consecutive identical digits, looping around
/// e.g. 611233546 -> 1+3+6 = 9
#[allow(dead_code)]
pub fn advent1_1(input : &String) -> u32 {
	advent_1(input, 1)
}

/// Given a string, calculates the sum of identical digits half around the string
/// e.g. 12131415 -> 1+1+1+1 = 4
#[allow(dead_code)]
pub fn advent1_2(input : &String) -> u32 {
	advent_1(input, input.len()/2)
}


/// Given a string and a step, calculates the sum of identical digits step places ahead, looping
#[allow(dead_code)]
fn advent_1(input : &String, step : usize) -> u32 {
	let mut counter : u32 = 0;
	let long = input.len();
	for x in 0..long {
		let goal = (x+step)%long ;
		let c = input[goal..goal+1].parse::<u32>().unwrap();
		let a = input[x..x+1].parse::<u32>().unwrap();
		if a == c { 
			counter += a;
		}			
	}
	counter
}

#[cfg(test)]
mod tests {
	use super::*;

	#[test]
	fn test1_1() {
		assert_eq!(3,advent1_1(&String::from("1122")))
	}

	#[test]
	fn test1_2() {
		assert_eq!(4,advent1_1(&String::from("1111")))
	}

	#[test]
	fn test1_3() {
		assert_eq!(0,advent1_1(&String::from("1234")))
	}

	#[test]
	fn test1_4() {
		assert_eq!(9,advent1_1(&String::from("91212129")))
	}

	#[test]
	fn test2_1() {
		assert_eq!(6,advent1_2(&String::from("1212")))
	}

	#[test]
	fn test2_2() {
		assert_eq!(4,advent1_2(&String::from("123425")))
	}

	#[test]
	fn test2_3() {
		assert_eq!(12,advent1_2(&String::from("123123")))
	}

	#[test]
	fn test2_4() {
		assert_eq!(4,advent1_2(&String::from("12131415")))
	}

	
}
