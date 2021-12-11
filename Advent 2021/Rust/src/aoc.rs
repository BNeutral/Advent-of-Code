#[allow(dead_code)]
pub fn to_vector(input : &str) -> Vec<i32> {
	let mut res = Vec::new();
	for line in input.lines() {
		res.push(line.parse::<i32>().unwrap());
	}
	res
}

#[allow(dead_code)]
pub fn to_2d_vector(input : &str) -> Vec<Vec<u32>> {
	let mut res = Vec::new();
	for line in input.lines() {
		let mut tiles = Vec::new();
		for ch in line.chars() {
			tiles.push(ch.to_digit(10).unwrap());
		}
		res.push(tiles);
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