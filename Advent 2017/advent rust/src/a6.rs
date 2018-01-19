use regex::Regex;
use std::collections::HashSet;
use std::collections::HashMap;

#[allow(dead_code)]
pub fn advent6_1(s : &str) -> u32 {
	let mut counter = 0;
	let mut vec = to_vector(s);
	let mut dic = HashSet::new();
	loop {
		if dic.contains(&vec) { break; }
		dic.insert(vec.clone());
		let mut max = 0;
		let mut max_pos = 0;
		for (pos, x) in vec.iter().enumerate() {
			if *x > max { 
				max_pos = pos;
				max = *x;
			}
		}
		vec[max_pos] = 0;
		for _ in 0..max {
			max_pos = (max_pos + 1) %	vec.len();
			vec[max_pos] += 1;	
		}
		counter += 1;
	}
	counter
}

#[allow(dead_code)]
pub fn advent6_2(s : &str) -> u32 {
	let mut counter : u32 = 0;
	let mut vec = to_vector(s);
	let mut dic = HashMap::new();
	loop {
		{
			let has_val = dic.get(&vec);
			if let Some(v) = has_val { 
				return counter-v;
			}
		}
		dic.insert(vec.clone(),counter);
		let mut max = 0;
		let mut max_pos = 0;
		for (pos, x) in vec.iter().enumerate() {
			if *x > max { 
				max_pos = pos;
				max = *x;
			}
		}
		vec[max_pos] = 0;
		for _ in 0..max {
			max_pos = (max_pos + 1) %	vec.len();
			vec[max_pos] += 1;	
		}
		counter += 1;
	}
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
