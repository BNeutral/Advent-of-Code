#[allow(dead_code)]
pub fn to_vector(input : &str) -> Vec<i32> {
	let mut res = Vec::new();
	for line in input.lines() {
		res.push(line.parse::<i32>().unwrap());
	}
	res
}

#[allow(dead_code)]
pub fn to_char_vec(input : &str) -> Vec<Vec<char>> {
	let mut res = Vec::new();
	for line in input.lines() {
		res.push(line.chars().collect());
	}
	res
}