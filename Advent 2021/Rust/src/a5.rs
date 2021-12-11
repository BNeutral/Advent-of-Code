use std::collections::HashMap;
use regex::Regex;

#[allow(dead_code)]
pub fn day5(input : &String) -> () {
	println!("Part1: {}", day5_1(&input));
	println!("Part2: {}", day5_2(&input));
}

pub fn day5_1(input : &String) -> i32 {
	solve(input, true)
}

pub fn day5_2(input : &String) -> i32 {
	solve(input, false)
}

pub fn solve(input : &String, ignore_diag : bool) -> i32 {
	let mut map = Map {
		map : HashMap::new()
	}; 
	for line in input.lines(){
		let map_line = Line::from_string(&line);
		map_line.mark_in_map(&mut map, ignore_diag);
	}
	map.count_overlaps()
}


#[derive(Debug)]
pub struct Map {
	map : HashMap<(i32,i32),i32>
}

impl Map {
	pub fn mark_cell(&mut self, position : (i32,i32)) {
		*self.map.entry(position).or_insert(0) += 1
	}

	pub fn count_overlaps(&self) -> i32 {
		let mut count = 0;
		for entry in self.map.values() {
			if *entry > 1 {
				count += 1;
			}
		}
		count
	}
}

#[derive(Copy, Clone, Debug, Hash)]
pub struct Line {
	p1 : (i32,i32),
	p2 : (i32,i32)
}

impl Line {
	fn from_string(input : &str) -> Line{
		let reg = Regex::new(r"(\d+),(\d+) -> (\d+),(\d+)").unwrap();

		let captures = reg.captures(input).unwrap();
		let n1 = captures.get(1).unwrap().as_str().parse::<i32>().unwrap();
		let n2 = captures.get(2).unwrap().as_str().parse::<i32>().unwrap();
		let n3 = captures.get(3).unwrap().as_str().parse::<i32>().unwrap();
		let n4 = captures.get(4).unwrap().as_str().parse::<i32>().unwrap();

		Line {
			p1: (n1,n2),
			p2: (n3,n4)
		}
	}

	fn mark_in_map(&self, map : &mut Map, ignore_diag : bool) {
		
		let p1x = std::cmp::min(self.p1.0,self.p2.0); 
		let p2x = std::cmp::max(self.p1.0,self.p2.0); 

		let p1y = std::cmp::min(self.p1.1,self.p2.1); 
		let p2y = std::cmp::max(self.p1.1,self.p2.1); 

		if self.p1.0 == self.p2.0 {
			for y in p1y..=p2y{
				map.mark_cell((self.p1.0,y));
			} 
							
		} else if self.p1.1 == self.p2.1 {
			for x in p1x..=p2x{
				map.mark_cell((x,self.p1.1));
			}
		} else if !ignore_diag {
			let mut go_vertical = 1;
			let mut start = self.p1;
			let mut end = self.p2;
			if self.p1.0 > self.p2.0 { // p2 is leftmost
				start = self.p2;	
				end = self.p1;
			}
			if start.1 > end.1 {
				go_vertical = -1;
			}
			let distance = end.0 - start.0;
			for z in 0..=distance{
				let x = start.0 + z;
				let y = start.1 + z*go_vertical; 
				map.mark_cell((x,y));
			}

		}
	}

}


#[cfg(test)]
mod tests {
	use super::*;

	#[test]
	fn test5_1() {
		let input = &String::from("0,9 -> 5,9\n8,0 -> 0,8\n9,4 -> 3,4\n2,2 -> 2,1\n7,0 -> 7,4\n6,4 -> 2,0\n0,9 -> 2,9\n3,4 -> 1,4\n0,0 -> 8,8\n5,5 -> 8,2\n");
		assert_eq!(5,day5_1(&input))
	}

	#[test]	
	fn test5_2() {
		let input = &String::from("0,9 -> 5,9\n8,0 -> 0,8\n9,4 -> 3,4\n2,2 -> 2,1\n7,0 -> 7,4\n6,4 -> 2,0\n0,9 -> 2,9\n3,4 -> 1,4\n0,0 -> 8,8\n5,5 -> 8,2\n");
		assert_eq!(12,day5_2(&input))
	}
}