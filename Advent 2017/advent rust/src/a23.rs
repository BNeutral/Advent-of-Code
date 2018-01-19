use regex::Regex;
use std::collections::HashSet;
use std::collections::HashMap;

#[allow(dead_code)]
pub fn advent23_1(s : &str) -> u32 {
	0
}

#[allow(dead_code)]
pub fn advent6_2(s : &str) -> u32 {
	0
}

fn to_vector(s : &str) -> Vec<u32> {
	let mut res = Vec::new();	
	let reg = Regex::new(r"(\d+)").unwrap();
	for m in reg.find_iter(s)
	{
		if let Ok(d) = m.as_str().parse::<u32>() 
		{
			res.push(d);
		}		
	}	
	res
}

#[cfg(test)]
mod tests {
	use super::*;

	#[test]
	fn test1() {
		assert_eq!(5,advent6_1("0 2 7 0"));
	}

	#[test]
	fn test2() {
		assert_eq!(4,advent6_2("0 2 7 0"));
	}

}
