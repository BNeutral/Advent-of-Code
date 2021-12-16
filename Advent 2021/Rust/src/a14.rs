use std::collections::HashMap;

#[allow(dead_code)]
pub fn day14(input : &String) -> () {
	println!("Part1: {}", solve(input, 10));
	println!("Part2: {}", solve(input, 40));
}

pub fn solve(input : &String, steps : u32) -> usize {
	let mut parsing_pairs = false;
	let mut pairs : HashMap<(char,char),char> = HashMap::new();
	let mut parsed_input : HashMap<(char,char),usize> = HashMap::new();
	let mut first_char = '*';

	for line in input.lines() {
		if line.is_empty() {
			parsing_pairs = true;
			continue;
		}

		if parsing_pairs {
			let split : Vec<&str> = line.split("->").collect();
			let inp : Vec<char> = split[0].trim().chars().collect();
			let pair : (char,char) = (inp[0],inp[1]);
			let res : char = split[1].trim().chars().next().unwrap(); 
			pairs.insert(pair, res);
		} else {
			let mut iter = line.chars();
			first_char = iter.next().unwrap();
			let mut prev_char = first_char;

			for ch in iter {
				let pair = (prev_char, ch);
				match parsed_input.get_mut(&pair) {
					Some(x) => *x += 1,
					_ => {
						parsed_input.insert(pair, 1);
					},
				}
				prev_char = ch;
			}
		}
	}


	for _ in 0..steps {
		let mut new_input : HashMap<(char,char),usize> = HashMap::new();

		for (key, amount) in parsed_input {
			let (first,second) = (key.0, key.1);

			match pairs.get(&(first,second)) {
				Some(middle_char) => {
					let p1 : (char,char) = (first, *middle_char);
					let p2 : (char,char) = (*middle_char, second);

					match new_input.get_mut(&p1) {
						Some(p) => { *p += amount; },
						_ => { new_input.insert(p1, amount); }
					}

					match new_input.get_mut(&p2) {
						Some(p) => { *p += amount; },
						_ => { new_input.insert(p2, amount); }
					}
				},
				_ => {},
			}
		}
		parsed_input = new_input;
	}

	count_min_max(&parsed_input, first_char)
}

fn count_min_max(input : &HashMap<(char,char),usize>, first_char : char) -> usize {
	let mut values : HashMap<char, usize> = HashMap::new();

	for (key, amount) in input {
		let ch2 = key.1;

		match values.get_mut(&ch2) {
			Some(x) => *x += amount,
			_ => {
				values.insert(ch2, *amount);
			}
		}
	}

	match values.get_mut(&first_char) {
		Some(x) => *x += 1,
		_ => {
			values.insert(first_char, 1);
		}
	}

	let min = values.values().min().unwrap();
	let max = values.values().max().unwrap(); 		

	max - min
}

#[cfg(test)]
mod tests {
	use super::*;

	#[test]
	fn test14_1() {
		let input = &String::from("NNCB\n\nCH -> B\nHH -> N\nCB -> H\nNH -> C\nHB -> C\nHC -> B\nHN -> C\nNN -> C\nBH -> H\nNC -> B\nNB -> B\nBN -> B\nBB -> N\nBC -> B\nCC -> N\nCN -> C\n");
		assert_eq!(1588,solve(input, 10));
	}

	#[test]
	fn test14_2() {
		let input = &String::from("NNCB\n\nCH -> B\nHH -> N\nCB -> H\nNH -> C\nHB -> C\nHC -> B\nHN -> C\nNN -> C\nBH -> H\nNC -> B\nNB -> B\nBN -> B\nBB -> N\nBC -> B\nCC -> N\nCN -> C\n");
		assert_eq!(2188189693529,solve(input, 40));
	}

}