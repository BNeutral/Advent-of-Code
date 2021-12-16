use std::collections::HashSet;
use regex::Regex;
use std::cmp::max;

#[allow(dead_code)]
pub fn day13(input : &String) -> () {
	println!("Part1: {}", solve(input, true));
	println!("Part2: {}", solve(input, false));
}

pub fn solve(input : &String, part_1 : bool) -> usize {
	let mut max_x = 0;
	let mut max_y = 0;
	let mut points : HashSet<(usize, usize)> = HashSet::new();  

	let mut commands : Vec<(&str, usize)> = Vec::new();
	let mut parsing_commands = false; 
	
	let reg = Regex::new(r"fold along ([xy])=(\d+)").unwrap();

	for line in input.lines() {
		if line.is_empty() {
			parsing_commands = true;
			continue;
		}

		if !parsing_commands {
			let split : Vec<&str> = line.split(',').collect();
			let point : (usize,usize) = (split[0].parse().unwrap(),split[1].parse().unwrap());
			max_x = max(max_x, point.0);
			max_y = max(max_y, point.1);
			points.insert(point);
		} else {
			let captures = reg.captures(line).unwrap();
			let axis = captures.get(1).unwrap().as_str();
			let value : usize = captures.get(2).unwrap().as_str().parse().unwrap();
			commands.push((axis,value));
		}
	}

	for command in commands {
		fold(&mut points, &mut max_x, &mut max_y, &command.0, command.1);
		if part_1 {
			break;
		}
	}

	if !part_1 {
		print(&points, max_x, max_y);
		0
	} else {
		points.len()
	}
}

fn fold(points : &mut HashSet<(usize, usize)>, max_x : &mut usize, max_y : &mut usize, axis : &str, fold_at : usize) {
	if axis == "x" {
		let dif = *max_x - fold_at;
		for y in 0..*max_y+1 {		
			for x in 1..dif+1 {
				let rx = fold_at + x;
				let r_point = (rx,y);
				if points.contains(&r_point) {
					points.remove(&r_point);
					points.insert((fold_at - x, y));
				}
			}
		}
		*max_x = fold_at - 1;
	} else if axis == "y" {
		let dif = *max_y - fold_at;
		for y in 1..dif+1 {		
			for x in 0..*max_x+1 {
				let dy = fold_at + y;
				let d_point = (x,dy);
				if points.contains(&d_point) {
					points.remove(&d_point);
					points.insert((x, fold_at - y));
				}
			}
		}
		*max_y = fold_at - 1;
	} else {
		panic!();
	}
}

fn print(points : &HashSet<(usize, usize)>, max_x : usize, max_y : usize) {
	println!("Fold with {} dots:",points.len());
	for y in 0..max_y+1 {
		let mut s = String::new();
		for x in 0..max_x+1 {
			if points.contains(&(x,y)) {
				s += "#";
			} else {
				s += "."
			}
		} 
		println!("{}",s);
	}
}  

#[cfg(test)]
mod tests {
	use super::*;

	#[test]
	fn test13_1() {
		let input = &String::from("6,10\n0,14\n9,10\n0,3\n10,4\n4,11\n6,0\n6,12\n4,1\n0,13\n10,12\n3,4\n3,0\n8,4\n1,10\n2,14\n8,10\n9,0\n\nfold along y=7\nfold along x=5\n");
		assert_eq!(17,solve(input, true));
	}

}