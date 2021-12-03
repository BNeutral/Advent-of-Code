use aoc::*;

#[allow(dead_code)]
pub fn day1(input : &String) -> () {
	let parsed = to_vector(input);
	println!("Part1: {}", day1_1(&parsed));
	println!("Part2: {}", day1_2(&parsed));
}


fn day1_1(input : &Vec<i32>) -> u32 {
	return solve(input, 1);
}

fn day1_2(input : &Vec<i32>) -> u32 {
	return solve(input, 3);
}


fn solve(input : &Vec<i32>, window_size : usize) -> u32 {
	let mut counter = 0;
	for i in 0..(input.len() - window_size) {
		let current = &input[i..(i+window_size)];
		let next = &input[(i+1)..(i+window_size+1)];
		let sum1 : i32 = current.iter().sum();
		let sum2 : i32 = next.iter().sum();
		if sum1 < sum2 {
			counter += 1; 
		}		
	} 
	counter
}

#[cfg(test)]
mod tests {
	use super::*;

	#[test]
	fn test1_1() {
		let input = &String::from("199\n200\n208\n210\n200\n207\n240\n269\n260\n263");
		let parsed = to_vector(input);
		assert_eq!(7,solve(&parsed, 1))
	}

	
	#[test]
	fn test1_2() {
		let input = &String::from("199\n200\n208\n210\n200\n207\n240\n269\n260\n263");
		let parsed = to_vector(input);
		assert_eq!(5,solve(&parsed, 3))
	}	
}
