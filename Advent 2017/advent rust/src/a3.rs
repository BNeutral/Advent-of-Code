use std::collections::HashMap;

#[derive(Clone, Copy, Debug)]
struct Num {
	n : u32,
	x : i32,
	y : i32,
}

impl Num{
	fn new(n : u32,x : i32,y : i32) -> Num {
		Num { n, x, y }
	}

	fn dist(&self) -> u32 {
		self.x.abs() as u32 + self.y.abs() as u32
	}
}

#[derive(Clone, Copy, Debug)]
enum Dir {
	Right = 0,
	Up = 1,
	Left = 2,
	Down = 3,
}

impl Dir{
	fn from_usize(i : usize) -> Dir { 
		[Dir::Right,Dir::Up,Dir::Left,Dir::Down][i%4] 
	}
}

#[allow(dead_code)]
pub fn advent3_1(n : u32) -> u32 {
	// [r,u,l,d]
	let mut steps = [1,1,2,2];
	let mut n_actual = Num::new(1,0,0);
	let mut cur_dir = Dir::Right;
	let mut contador = steps[Dir::Right as usize];
	for x in 1..n {
		contador -= 1;
		n_actual.n = x;
		match cur_dir {
			Dir::Right => {
				n_actual.x += 1;
			}
			Dir::Up => {
				n_actual.y += 1;
			}
			Dir::Left => {
				n_actual.x -= 1;
			}
			Dir::Down => {
				n_actual.y -= 1;
			}
		}
		if contador <= 0 {
			steps[cur_dir as usize] += 2;
			cur_dir = Dir::from_usize(cur_dir as usize + 1);
			contador = steps[cur_dir as usize];
		}
	}
	n_actual.dist()
}

#[allow(dead_code)]
pub fn advent3_2(n : u32) -> u32 {
	// [r,u,l,d]
	let mut steps = [1,1,2,2];
	let mut n_actual = Num::new(1,0,0);
	let mut cur_dir = Dir::Right;
	let mut contador = steps[Dir::Right as usize];
	let mut dict : HashMap<(i32,i32),Num> = HashMap::new();
	dict.insert((n_actual.x,n_actual.y),n_actual);
	while n_actual.n <= n {
		contador -= 1;
		match cur_dir {
			Dir::Right => {
				n_actual.x += 1;
			}
			Dir::Up => {
				n_actual.y += 1;
			}
			Dir::Left => {
				n_actual.x -= 1;
			}
			Dir::Down => {
				n_actual.y -= 1;
			}
		}
		if contador <= 0 {
			steps[cur_dir as usize] += 2;
			cur_dir = Dir::from_usize(cur_dir as usize + 1);
			contador = steps[cur_dir as usize];
		}
		n_actual.n = {
			let mut result : u32 = 0;
			for x in n_actual.x-1..n_actual.x+2 {
				for y in n_actual.y-1..n_actual.y+2 {
					if x == n_actual.x && y == n_actual.y { continue; }
					match dict.get(&(x,y)) {
						Some(v) => { result += v.n }
						_ => {}
					}
				}
			}
			result
		};
		dict.insert((n_actual.x,n_actual.y),n_actual);
	}
	n_actual.n
}

#[cfg(test)]
mod tests {
	use super::*;

	#[test]
	fn test1() {
		assert_eq!(0,advent3_1(1));
	}
	
	#[test]
	fn test2() {
		assert_eq!(3,advent3_1(12));
	}

	#[test]
	fn test3() {
		assert_eq!(2,advent3_1(23));
	}

	#[test]
	fn test4() {
		assert_eq!(31,advent3_1(1024));
	}

	#[test]
	fn test5() {
		assert_eq!(2,advent3_2(1));
	}

	#[test]
	fn test6() {
		assert_eq!(4,advent3_2(2));
		assert_eq!(5,advent3_2(4));
		assert_eq!(10,advent3_2(5));
		assert_eq!(11,advent3_2(10));
		assert_eq!(23,advent3_2(11));
		assert_eq!(25,advent3_2(23));
		assert_eq!(26,advent3_2(25));
		assert_eq!(54,advent3_2(26));
		assert_eq!(57,advent3_2(54));
		assert_eq!(59,advent3_2(57));
		assert_eq!(122,advent3_2(59));
		assert_eq!(133,advent3_2(122));
		assert_eq!(142,advent3_2(133));
		assert_eq!(147,advent3_2(142));
		assert_eq!(304,advent3_2(147));
		assert_eq!(330,advent3_2(304));
		assert_eq!(351,advent3_2(330));
		assert_eq!(362,advent3_2(351));
		assert_eq!(747,advent3_2(362));
		assert_eq!(806,advent3_2(747));
	}

}
