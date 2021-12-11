use std::collections::HashMap;
use std::collections::HashSet;

const EMPTY_STRING: String = String::new();

#[allow(dead_code)]
pub fn day8(input : &String) -> () {
	println!("Part1: {}", day8_1(input));
	println!("Part2: {}", day8_2(input));
}

pub fn day8_1(input : &String) -> i32 {
	let mut unique_counter = 0;

	for line in input.lines() {
		let split = line.split("|").collect::<Vec<&str>>();
		let end_digits : Vec<String> = split[1].trim().split_whitespace().map(sort_string).collect();

		for display in end_digits {
			match match_number_1(&display) {
				Some(_) => unique_counter += 1,
				_ => {}
			}

		}
	}
	unique_counter
}

pub fn day8_2(input : &String) -> i32 {
	let mut outputs: Vec<i32> = Vec::new();

	for line in input.lines() {
		let split = line.split("|").collect::<Vec<&str>>();

		let start_digits : Vec<String> = split[0].trim().split_whitespace().map(sort_string).collect();
		let end_digits : Vec<String> = split[1].trim().split_whitespace().map(sort_string).collect();

		let mut known : [String;10] = [EMPTY_STRING;10];
		let mut known_lookup : HashMap<String, usize> = HashMap::new(); 

		while known_lookup.len() < 10 {
			for digit in &start_digits{
				match match_number_2(&digit, &known, &known_lookup) {
					Some(x) => {
						known[x] = digit.to_owned();
						known_lookup.insert(digit.to_owned(), x);
					}
					_ => {}
				}
			}
		}

		let result = to_number(&end_digits, &known_lookup);
		outputs.push(result);

	}

	outputs.iter().sum()
}

fn match_number_1(input : &String) -> Option<usize> {
	match input.len() {
		2 => Some(1),
		4 => Some(4),
		3 => Some(7),
		7 => Some(8),
		_ => None
	}
}

fn match_number_2(input : &String, known: &[String;10], known_lookup : &HashMap<String, usize>) -> Option<usize> {
	if known_lookup.contains_key(input) {
		return Some(*known_lookup.get(input).unwrap());
	}

	match input.len() {
		2 => Some(1),
		3 => Some(7),
		4 => Some(4),
		5 => {
			if !known[1].is_empty() {
				if str_contains(input, &known[1]){
					return Some(3);
				} 
			}
			if !known[6].is_empty() {
				let diff =  str_difference(&known[6], input);
				if diff.len() == 1 {
					return Some(5);
				} else if diff.len() == 2 {
					return Some(2);
				}
			}
			None
		}
		6 => {
			if !known[1].is_empty() {
				if !str_contains(input, &known[1]){
					return Some(6);
				}
			}	
			if !known[4].is_empty() && !known[3].is_empty() {
				if str_contains(input, &known[3]) && str_contains(input, &known[4]){
					return Some(9);
				}
			} 
			if !known[1].is_empty() && !known[4].is_empty() && !known[3].is_empty() {
				return Some(0);
			}
			None
		}
		7 => Some(8),
		_ => None
	}
}

// -- Oh no, the I couldn't find what I needed in the std so I had to make some awful string functions
// Also the hashsets were annoying between all the parsing and conversions and unwrapping and etc

fn str_contains(input : &String, substring : &String) -> bool {
	let chars : HashSet<char> = input.chars().collect();
	for cha in substring.chars() {
		if !chars.contains(&cha) {
			return false;
		}
	}
	true
}

fn str_difference(input1 : &String, input2 : &String) -> String {
	let mut chars : HashSet<char> = input1.chars().collect();
	for cha in input2.chars() {
		chars.remove(&cha);
	}
	sort_string(chars.iter().collect::<String>().as_str())
}

fn sort_string(input : &str) -> String {
	let mut letters : Vec<char> = input.chars().collect();
	letters.sort();
	letters.iter().collect() 
}

fn to_number(inputs : &Vec<String>, known_lookup : &HashMap<String, usize>) -> i32 {
	let mut num : String = "".to_owned();
	for digit in inputs {
		num = num + &known_lookup.get(digit).unwrap().to_string();
	}
	num.parse().unwrap()
}

#[cfg(test)]
mod tests {
	use super::*;

	#[test]
	fn test8_1() {
		let input = &String::from("be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe\nedbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec |fcgedb cgb dgebacf gc\nfgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef |cg cg fdcagb cbg\nfbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega |efabcd cedba gadfec cb\naecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga |gecf egdcabf bgf bfgea\nfgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf |gebdcfa ecba ca fadegcb\ndbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf |cefg dcbef fcge gbcadfe\nbdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd |ed bcgafe cdgba cbgef\negadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg |gbdfcae bgc cg cgb\ngcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc |fgae cfgab fg bagce");
		assert_eq!(26,day8_1(&input))
	}

	#[test]	
	fn test8_2() {
		let input = &String::from("acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf");
		assert_eq!(5353,day8_2(&input))
	}

	#[test]	
	fn test8_3() {
		let input = &String::from("be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe");
		assert_eq!(8394,day8_2(&input))
	}	

	#[test]	
	fn test8_4() {
		let input = &String::from("be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe\nedbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec |fcgedb cgb dgebacf gc\nfgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef |cg cg fdcagb cbg\nfbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega |efabcd cedba gadfec cb\naecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga |gecf egdcabf bgf bfgea\nfgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf |gebdcfa ecba ca fadegcb\ndbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf |cefg dcbef fcge gbcadfe\nbdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd |ed bcgafe cdgba cbgef\negadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg |gbdfcae bgc cg cgb\ngcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc |fgae cfgab fg bagce");
		assert_eq!(61229,day8_2(&input))
	}

}