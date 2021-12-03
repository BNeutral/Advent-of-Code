use aoc::*;

#[allow(dead_code)]
pub fn day3(input : &String) -> () {
	let parsed = to_char_vec(input);
	println!("Part1: {}", day3_1(&parsed));
	println!("Part2: {}", day3_2(&parsed));
}

pub fn day3_1(input : &Vec<Vec<char>>) -> u32 {
	let line_len = input[0].len();
	let mut gamma : u32 = 0;
	let mut epsilon : u32 = 0;

	for digit_position in 0..line_len {
		let pos_from_right = line_len - 1 - digit_position;
		if find_most_common_in_pos_from_left(input, digit_position) == '1' {
			gamma = set_bit(gamma, pos_from_right);
		} else {
			epsilon = set_bit(epsilon, pos_from_right);
		}
	}

	// println!("gamme {:b}",gamma);
	// println!("epsilon {:b}",epsilon);
	gamma * epsilon 
}

fn find_most_common_in_pos_from_left(input : &Vec<Vec<char>>, position : usize) -> char {
	let mut ones = 0;
	let mut zeros = 0;

	for line in input {
		let ch = line[position];
		match ch {
			'0' => zeros += 1,
			'1' => ones += 1,
			_ => panic!()
		}
	}
	
	if ones >= zeros {
		'1'
	}
	else {
		'0'
	}
}

fn set_bit(number : u32, position_from_right : usize) -> u32 {
	number | (1 << position_from_right)
}

fn number_from_char_vec(input : &Vec<char>) -> u32 {
	let mut num = 0;
	for x in 0..input.len(){
		let from_right = input.len() - 1 - x;
		if input[x] == '1' {
			num |= 1 << from_right; 
		}
	}
	num
}
 

pub fn day3_2(input : &Vec<Vec<char>>) -> u32 {
	let mut filtered_ox = input.clone();
	let mut digit_position = 0;
	while filtered_ox.len() > 1{
		let most_common = find_most_common_in_pos_from_left(&filtered_ox, digit_position);
		filtered_ox.retain(|num| num[digit_position] == most_common);
		digit_position += 1;	
	}
	let oxy_gen = number_from_char_vec(&filtered_ox[0]);
	
	let mut filtered_co = input.clone();
	let mut digit_position = 0;
	while filtered_co.len() > 1{
		let most_common = find_most_common_in_pos_from_left(&filtered_co, digit_position);
		filtered_co.retain(|num| num[digit_position] != most_common);
		digit_position += 1;	
	}
	let co2_scrub = number_from_char_vec(&filtered_co[0]);

	//println!("oxy {:b}",oxy_gen);
	//println!("co2 {:b}",co2_scrub);
	oxy_gen * co2_scrub
}



#[cfg(test)]
mod tests {
	use super::*;

	#[test]
	fn test3_1() {
		let input = &String::from("00100\n11110\n10110\n10111\n10101\n01111\n00111\n11100\n10000\n11001\n00010\n01010");
		let parsed = to_char_vec(input);
		assert_eq!(198,day3_1(&parsed))
	}

	
	#[test]
	fn test3_2() {
		let input = &String::from("00100\n11110\n10110\n10111\n10101\n01111\n00111\n11100\n10000\n11001\n00010\n01010");
		let parsed = to_char_vec(input);
		assert_eq!(230,day3_2(&parsed))
	}
}