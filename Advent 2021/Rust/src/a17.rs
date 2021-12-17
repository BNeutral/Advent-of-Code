use regex::Regex;
//use std::collections::HashSet;

#[allow(dead_code)]
pub fn day17(input : &String) -> () {
	println!("Part1: {}", day17_1(input));
	println!("Part2: {}", day17_2(input));
}

pub fn day17_1(input : &String) -> i32 {
	let area = TargetArea::new(input);	
	// Optimal start vel is such that it ends on the lower bound of the area
	// After returning to 0, which takes steps equal to the initial velocity
	let mut probe = Probe::new( (0, -(area.y_min+1) ));
	probe.find_y_max(&area)
}

pub fn day17_2(input : &String) -> i32 {
	let area = TargetArea::new(input);	
	let mut counter = 0;

	for vx in 0..area.x_max+1 {
		for vy in area.y_min..-area.y_min {
			let mut probe = Probe::new((vx, vy));
			if probe.step_until_oob(&area) {
				counter += 1;
			}
		}
	}

	counter
}

#[derive(Debug)]
struct TargetArea {
	x_min : i32,
	x_max : i32,
	y_min : i32,
	y_max : i32
}

impl TargetArea{
	pub fn new(input : &String) -> TargetArea {
		let reg = Regex::new(r"target area: x=([-]?\d+)..([-]?\d+), y=([-]?\d+)..([-]?\d+)").unwrap();
		let captures = reg.captures(input).unwrap();

		let area = TargetArea {
			x_min : captures.get(1).unwrap().as_str().parse().unwrap(),
			x_max : captures.get(2).unwrap().as_str().parse().unwrap(),
			y_min : captures.get(3).unwrap().as_str().parse().unwrap(),
			y_max : captures.get(4).unwrap().as_str().parse().unwrap(),
		};

		area
	}
}

#[derive(Debug)]
struct Probe {
	pos : (i32,i32),
	vel : (i32,i32)
}

impl Probe {
	pub fn new(vel : (i32,i32)) -> Probe {
		let probe = Probe {
			pos : (0,0),
			vel : vel
		};
		probe
	}

	pub fn step(&mut self) {
		self.pos.0 += self.vel.0;
		self.pos.1 += self.vel.1;
		if self.vel.0 > 0 {
			self.vel.0 -= 1;
		} else if self.vel.0 < 0 {
			self.vel.0 += 1;
		}
		self.vel.1 -= 1;
	}

	pub fn step_until_oob(&mut self, target : &TargetArea) -> bool {
		loop {
			self.step();
			if self.pos.0 >= target.x_min && self.pos.0 <= target.x_max && self.pos.1 >= target.y_min && self.pos.1 <= target.y_max {
				return true;
			} 
			if self.vel.0 == 0 && (self.pos.0 < target.x_min || self.pos.0 > target.x_max) {
				return false;
			}		
			if self.pos.1 < target.y_min {
				return false;
			}	
		}
	}

	pub fn find_y_max(&mut self, target : &TargetArea) -> i32 {
		let mut max_height = 0;
		loop {
			self.step();
			max_height = std::cmp::max(self.pos.1, max_height);
			if self.pos.1 >= target.y_min && self.pos.1 <= target.y_max {
				return max_height;
			} 
			if self.pos.1 < target.y_min {
				return 0;
			}		
		}
	}

}

#[cfg(test)]
mod tests {
	use super::*;

	#[test]
	fn test17_1() {
		let input = &String::from("target area: x=20..30, y=-10..-5");
		assert_eq!(45,day17_1(input));
	}

	#[test]
	fn test17_2() {
		let input = &String::from("target area: x=20..30, y=-10..-5");
		assert_eq!(112,day17_2(input));
	}
}