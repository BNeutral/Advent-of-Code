use std::cmp::*;

#[allow(dead_code)]
pub fn day7(input : &String) -> () {
	println!("Part1: {}", day7_1(input));
	println!("Part2: {}", day7_2(input));
}

pub fn day7_1(input : &String) -> i32 {
	let (crabs, crab_min, crab_max) = parse(input);

	let mut best_fuel = i32::MAX;
	for position in crab_min..crab_max {
		let distance_to : i32= crabs.iter().map(|pos| i32::abs(pos - position)).sum();
		best_fuel = min(best_fuel, distance_to);
	} 	
	best_fuel
}

pub fn day7_2(input : &String) -> i32 {
	let (crabs, crab_min, crab_max) = parse(input);

	let mut best_fuel = i32::MAX;
	for position in crab_min..crab_max {
		let distance_to : i32 = crabs.iter().map(
			|pos| { 
			let dist = i32::abs(pos - position);
			dist * (dist+1) / 2 
		}).sum();
		best_fuel = min(best_fuel, distance_to);
	} 	
	best_fuel
}

fn parse(input : &String) -> (Vec<i32>, i32, i32) {
	let mut crabs : Vec<i32> = Vec::new();
	let mut crab_min = i32::MAX;
	let mut crab_max = i32::MIN;

	for a_crab in input.split(',') {
		let pos = a_crab.parse::<i32>().unwrap();
		crabs.push(pos);
		crab_min = min(pos, crab_min);
		crab_max = max(pos, crab_max);
	}

	(crabs, crab_min, crab_max)
} 

#[cfg(test)]
mod tests {
	use super::*;

	#[test]
	fn test7_1() {
		let input = &String::from("16,1,2,0,4,2,7,1,2,14");
		assert_eq!(37,day7_1(&input))
	}

	#[test]	
	fn test7_2() {
		let input = &String::from("16,1,2,0,4,2,7,1,2,14");
		assert_eq!(168,day7_2(&input))
	}
}