#[allow(dead_code)]
pub fn day6(input : &String) -> () {
	println!("Part1: {}", day6_1(&input));
	println!("Part2: {}", day6_2(&input));
}

pub fn day6_1(input : &String) -> i64 {
	solve(input, 80)
}

pub fn day6_2(input : &String) -> i64 {
	solve(input, 256)
}

pub fn solve(input : &String, simulation_days : i32) -> i64 {
	let mut fish : [i64; 9] = [0; 9];

	for a_fish in input.split(',') {
		let days = a_fish.parse::<usize>().unwrap();
		fish[days] += 1;
	}

	for _ in 0..simulation_days{
		let mut new_fish : [i64; 9] = [0; 9];

		for x in 0..fish.len() {
			if x == 0 {
				new_fish[6] += fish[x];
				new_fish[8] += fish[x];
			} else {
				new_fish[x-1] += fish[x]
			}
		}

		fish = new_fish;
	}	
	
	fish.iter().sum()
}

#[cfg(test)]
mod tests {
	use super::*;

	#[test]
	fn test6_1() {
		let input = &String::from("3,4,3,1,2");
		assert_eq!(5934,day6_1(&input))
	}

	#[test]	
	fn test6_2() {
		let input = &String::from("3,4,3,1,2");
		assert_eq!(26984457539,day6_2(&input))
	}
}