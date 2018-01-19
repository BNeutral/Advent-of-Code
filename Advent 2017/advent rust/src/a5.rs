#[allow(dead_code)]
pub fn advent5_1(s : &str) -> u32 {
	let mut vec = to_vector(s);
	let mut pc : i32 = 0;
	let mut jmpcnt = 0;
	let len = vec.len();
	loop {
		if pc as usize > len-1 { break }
		jmpcnt += 1;
		let jmp = vec[pc as usize];
		vec[pc as usize] += 1;
		pc += jmp;
	}
	jmpcnt
}

#[allow(dead_code)]
pub fn advent5_2(s : &str) -> u32 {
	let mut vec = to_vector(s);
	let mut pc : i32 = 0;
	let mut jmpcnt = 0;
	let len = vec.len();
	loop {
		if pc as usize > len-1 { break }
		jmpcnt += 1;
		let jmp = vec[pc as usize];
		if jmp >= 3 { vec[pc as usize] -= 1; }
		else { vec[pc as usize] += 1; }
		pc += jmp;
	}
	jmpcnt
}

fn to_vector(s : &str) -> Vec<i32> {
	let mut res = Vec::new();
	for s in s.lines() {
		res.push(s.parse::<i32>().unwrap());
	}
	res
}

#[cfg(test)]
mod tests {
	use super::*;

	#[test]
	fn test1() {
		assert_eq!(5,advent5_1("0\n3\n0\n1\n-3"));
	}

	#[test]
	fn test2() {
		assert_eq!(10,advent5_2("0\n3\n0\n1\n-3"));
	}
}
