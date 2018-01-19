use regex::Regex;

#[allow(dead_code)]
pub fn advent2_1(s : &String) -> u32 {
	let mut result = 0;
	let reg = Regex::new(r"(\d+)").unwrap();
	for string in s.lines() 
	{	
		let mut min : u32 = u32::max_value();
		let mut max : u32 = 0;
		for m in reg.find_iter(string)
		{
			if let Ok(d) = m.as_str().parse::<u32>() 
			{
				if d < min { min = d; }
				if d > max { max = d; }
			}		
		}	
		result += max - min;
	}	
	result
}

#[allow(dead_code)]
pub fn advent2_2(s : &String) -> u32 {
	let mut result = 0;
	let reg = Regex::new(r"(\d+)").unwrap();
	for string in s.lines() 
	{	
		let mut nums = Vec::new(); 
		for m in reg.find_iter(string)
		{
			if let Ok(d) = m.as_str().parse::<u32>() 
			{
				nums.push(d);
			}		
		}
		for x in 0..nums.len()
		{
			for y in x+1..nums.len()
			{
				let a = nums[x];
				let b = nums[y];
				if a%b == 0 { result += a/b; }
				if b%a == 0 { result += b/a; }
			}
		}
	}	
	result
}



#[cfg(test)]
mod tests {
	use super::*;

	#[test]
	fn test1() {
		assert_eq!(18,advent2_1(&String::from("5 1 9 5\n7 5 3\n2 4 6 8")))
	}
	
	#[test]
	fn test2() {
		assert_eq!(9,advent2_2(&String::from("5 9 2 8\n9 4 7 3\n3 8 6 5")))
	}

}
