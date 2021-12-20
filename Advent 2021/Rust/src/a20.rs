use aoc::*; 
use std::collections::HashSet;
use std::cmp::*;
use std::fmt;

#[allow(dead_code)]
pub fn day20(input : &String) -> () {
	println!("Part1: {}", day20_1(input));
	println!("Part2: {}", day20_2(input));
}

pub fn day20_1(input : &String) -> i32 {
	solve(input,2)
}

pub fn day20_2(input : &String) -> i32 {
	solve(input,50)
}

pub fn solve(input : &String, steps : usize) -> i32 {
	let mut bits = BitVec::new();
	let mut image = InfiniteImage::new();
	let mut image_line_counter = 0;

	let mut parsing_image = false;
	for line in input.lines() {
		if parsing_image {
			image.add_line(line, 0, image_line_counter);
			image_line_counter += 1;
		}
		if line.is_empty() {
			parsing_image = true;
		} else if !parsing_image {
			bits = BitVec::from_20(line);			
		}
	}

	if bits.get_bit(0) == 1 && bits.get_bit(511) != 0 {
		panic!("Unsolvable nonsense without some heavy ass math");
	}
	let flips_border = bits.get_bit(0) == 1 && bits.get_bit(511) == 0;
	for x in 0..steps {
		image = image.enhance(&bits, flips_border, x);
	} 

	image.pixels.len() as i32
}



impl BitVec {
	pub fn from_20(input : &str) -> BitVec {
		let mut counter = 0;

		let mut bits = BitVec::new_sized(512);

		for ch in input.chars() {
			if ch == '#' {
				bits.set_bit(counter);
			}
			counter += 1;
		}

		bits
	}
}

struct InfiniteImage {
	pixels : HashSet<(i32, i32)> 
}

impl InfiniteImage {
	pub fn new() -> InfiniteImage {
		InfiniteImage {
			pixels : HashSet::new()
		}
	}

	pub fn add_line(&mut self, line : &str, mut x : i32, y : i32) {
		for ch in line.chars() {
			if ch == '#' {
				self.pixels.insert((x,y));
			}
			x += 1;
		}
	}

	pub fn find_corners(&self) -> (i32,i32,i32,i32) {
		let mut x_min = i32::MAX;
		let mut x_max = i32::MIN;
		let mut y_min = i32::MAX;
		let mut y_max = i32::MIN;
		for pixel in self.pixels.iter() {
			x_min = min(x_min, pixel.0);
			x_max = max(x_max, pixel.0);
			y_min = min(y_min, pixel.1);
			y_max = max(y_max, pixel.1);
		}
		(x_min, x_max, y_min, y_max)
	}

	pub fn enhance(&self, algo : &BitVec, flips_border : bool, iteration : usize) -> InfiniteImage {
		let mut new = InfiniteImage::new();

		let (x_min, x_max, y_min, y_max) = self.find_corners();

		for y in y_min-1..y_max+2 {
			for x in x_min-1..x_max+2 {
				self.enhance_pixel(x, y, algo, &mut new, x_min, x_max, y_min, y_max, flips_border, iteration);
			}
		}

		new
	}

	pub fn enhance_pixel(&self, x:i32, y:i32, algo : &BitVec, new_image : &mut InfiniteImage, x_min : i32, x_max : i32, y_min : i32, y_max : i32, flips_border : bool, iteration : usize) {
		let mut num = BitVec::new_sized(9);
		let mut count = 0;
		let surrounding = get_sorrounding_in_order(x, y);
		for point in surrounding {
			let px = point.0;
			let py = point.1;
			if self.pixels.contains(&point) {
				num.set_bit(count);
			}
			if flips_border && iteration % 2 == 1 && (px < x_min || px > x_max || py < y_min || py > y_max) {
				num.set_bit(count);
			}
			count += 1;
		}
		let pos = num.get_bits(0, 9) as usize;
		if algo.get_bit(pos) == 1 {
			new_image.pixels.insert((x,y));
		} 
	}

}

fn get_sorrounding_in_order(x : i32, y : i32) -> Vec<(i32, i32)> {
	let mut res : Vec<(i32,i32)> = Vec::new();
	for py in y-1..y+2 {
		for px in x-1..x+2 {
			res.push((px,py));
		} 
	}
	res 
}

impl fmt::Display for InfiniteImage {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
		let (x_min, x_max, y_min, y_max) = self.find_corners();
		let mut res : fmt::Result = fmt::Result::Ok(());
		for y in y_min..y_max+1 {
			for x in x_min..x_max+1 {
				if self.pixels.contains(&(x,y)) {
					res = write!(f, "#");
				} else {
					res = write!(f, ".");
				}
				match res {
					fmt::Result::Err(_) => return res,
					_ => {}
				}
			}
			res = write!(f, "\n");
			match res {
				fmt::Result::Err(_) => return res,
				_ => {}
			}
		}
		res
    }
}

#[cfg(test)]
mod tests {
	use super::*;
	
	#[test]
	fn test20_1() {
		let input = String::from("..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#\n\n#..#.\n#....\n##..#\n..#..\n..###");
		assert_eq!(35, day20_1(&input));
	}

	#[test]
	fn test19_2() {
		let input = String::from("..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#\n\n#..#.\n#....\n##..#\n..#..\n..###");
		assert_eq!(3351, day20_2(&input));
	}
}