use std::collections::HashSet;
use std::collections::HashMap;
use regex::Regex;

#[allow(dead_code)]
pub fn is_valid(s : &str) -> bool {
	let mut dict = HashSet::new();
	let reg = Regex::new(r"([^ ]+)").unwrap();
	for substr in reg.find_iter(s)
	{
		let sub = substr.as_str();
		if dict.contains(sub) { return false }
		dict.insert(sub);
	}	
	true
}

#[allow(dead_code)]
pub fn is_valid_anag(s : &str) -> bool {
	let mut dict : HashSet<Box<&str>> = HashSet::new();
	let reg = Regex::new(r"([^ ]+)").unwrap();
	for substr in reg.find_iter(s)
	{
		let sub = substr.as_str();
		for x in dict.iter() {
			if is_anagram(x,sub) { return false }
		}
		dict.insert(Box::new(sub));
	}
	true
}

#[allow(dead_code)]
pub fn is_anagram(s1 : &str, s2 : &str) -> bool {
	if s1.len() != s2.len() { return false }
	let d1 = to_dict(s1);
	let d2 = to_dict(s2);
	d1 == d2
}

#[allow(dead_code)]
pub fn to_dict(s : &str) ->  HashMap<char,u32> {
	let mut dict : HashMap<char,u32> = HashMap::new();
	for c in s.chars() {
		match dict.get(&c) {
			Some(&v) => { dict.insert(c, v+1); }
			None => { dict.insert(c, 1); }
		}
	}
	dict
}

#[allow(dead_code)]
pub fn advent4_1(s : &String) -> u32 {
	let mut contador = 0;
	for string in s.lines() 
	{
		if is_valid(string) { contador += 1; }
	}	
	contador
}

#[allow(dead_code)]
pub fn advent4_2(s : &String) -> u32 {
	let mut contador = 0;
	for string in s.lines() 
	{
		if is_valid_anag(string) { contador += 1; }
	}	
	contador
}

#[cfg(test)]
mod tests {
	use super::*;

	#[test]
	fn test1() {
		assert!(is_valid("aa bb cc"));
	}

	#[test]
	fn test2() {
		assert!(!is_valid("aa bb cc aa"));
	}

	#[test]
	fn test3() {
		assert!(is_valid("aa bb cc aaa"));
	}

	#[test]
	fn test4() {
		assert_eq!(2,advent4_1(&String::from("aa bb cc\naa bb cc aa\naa bb cc aaa")));
	}

	#[test]
	fn test_anagrama() {
		assert!(is_anagram("asdfa","fdsaa"));
		assert!(!is_anagram("asdfg","fdsaa"));
	}

	#[test]
	fn test_valid_anag() {
		assert!(!is_valid_anag("asdfa fdsaa"));
		assert!(is_valid_anag("asdfg fdsaa"));
	}

	#[test]
	fn test5() {
		assert_eq!(2,advent4_2(&String::from("aa bb cc\naca bb cc aca\naa bb cc aaa")));
	}
}
