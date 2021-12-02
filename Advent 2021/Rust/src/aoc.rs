

#[allow(dead_code)]
pub fn to_vector(s : &str) -> Vec<i32> {
	let mut res = Vec::new();
	for s in s.lines() {
		res.push(s.parse::<i32>().unwrap());
	}
	res
}