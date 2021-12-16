extern crate priority_queue;

use aoc::*;
use std::collections::HashSet;
use self::priority_queue::DoublePriorityQueue;

#[allow(dead_code)]
pub fn day15(input : &String) -> () {
	println!("Part1: {}", day15_1(input));
	println!("Part2: {}", day15_2(input));
}

pub fn day15_1(input : &String) -> u32 {
	let map = to_2d_vector(input);
	solve(&map)
}

pub fn day15_2(input : &String) -> u32 {
	let mut map = to_2d_vector(input);

	let orig_leny = map.len();
	let orig_lenx = map[0].len();

	let new_len_y = orig_leny*5;
	let new_len_x = orig_lenx*5;


	map.resize(new_len_y, Vec::new());
	for row in map.iter_mut() {
		row.resize(new_len_x, 0);
	}

	// A "better" solution would be to extract this so it's calculated on demand
	// But the input is small enough that it doesn't matter
	for y in 0..new_len_y {
		for x in 0..new_len_x {
			let risk_inc = x / orig_lenx + y / orig_leny;
			let ox = x % orig_lenx;
			let oy = y % orig_leny;
			let mut val = (map[oy][ox] + risk_inc as u32) % 9;
			if val == 0 {
				val = 9;
			} 
			map[y][x] = val;
		}
	}

	solve(&map)
}

pub fn solve(map : &Vec<Vec<u32>>) -> u32 {
	let leny = map.len();
	let lenx = map[0].len();

	let mut visited : HashSet<(usize,usize)> = HashSet::new();
	let mut priority_queue : DoublePriorityQueue<(usize,usize), u32> = DoublePriorityQueue::new();

	let mut min_risk = map.clone();
	for y in 0..leny {
		for x in 0..lenx {
			min_risk[y][x] = u32::MAX;
		}
	}

	priority_queue.push((0,0), 0);
	
	// Because the priority is by max instead of min in this priority queue implementation, we'll pass negative numbers
	while !priority_queue.is_empty() {
		let ((x,y), dist) = priority_queue.pop_min().unwrap();
		visited.insert((x,y));
		min_risk[y][x] = dist;

		let mut nodes : Vec<(usize, usize)> = Vec::new();
		if x > 0 {
			nodes.push( (x-1,y) );
		}
		if x < lenx-1 {
			nodes.push( (x+1,y) );
		}
		if y > 0 {
			nodes.push( (x,y-1) );
		}
		if y < leny-1 {
			nodes.push( (x,y+1) );
		}

		for node in nodes {
			if visited.contains(&node) {
				continue;
			}
			let d = map[node.1][node.0] + dist;
			priority_queue.push_decrease(node, d); 
		}

	}

	min_risk[lenx-1][leny-1]
}




#[cfg(test)]
mod tests {
	use super::*;

	#[test]
	fn test15_1() {
		let input = &String::from("1163751742\n1381373672\n2136511328\n3694931569\n7463417111\n1319128137\n1359912421\n3125421639\n1293138521\n2311944581\n");
		assert_eq!(40,day15_1(input));
	}

	#[test]
	fn test15_2() {
		let input = &String::from("1163751742\n1381373672\n2136511328\n3694931569\n7463417111\n1319128137\n1359912421\n3125421639\n1293138521\n2311944581\n");
		assert_eq!(315,day15_2(input));
	}

}