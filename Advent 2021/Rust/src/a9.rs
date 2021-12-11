use aoc::*;
use std::collections::HashSet;

#[allow(dead_code)]
pub fn day9(input : &String) -> () {
	let height_map = to_2d_vector(input);
	println!("Part1: {}", day9_1(&height_map));
	println!("Part2: {}", day9_2(&height_map));
}

pub fn day9_1(height_map : &Vec<Vec<u32>>) -> u32 {
	let mut risk = 0;
	let mins = get_mins(height_map);

	for min in mins {
				risk += get_risk(&height_map, min);
	}

	risk
}

#[derive(Debug, Clone, Copy, PartialEq)]
enum Direction {
	UP,
	DOWN,
	LEFT,
	RIGHT,
	NOP
}

fn get_risk(height_map : &Vec<Vec<u32>>, (x,y) : (usize, usize)) -> u32 {
	match get_tile(height_map, (x, y), Direction::NOP) {
		Some(z) => 1 + z,
		_ => 0
	}
} 

fn get_tile_pos(height_map : &Vec<Vec<u32>>, (mut x, mut y) : (usize, usize), dir : Direction) -> Option<(usize,usize)> {
	match dir {
		Direction::UP => {
			if y == 0 {
				return None
			}
			y -= 1}, 
		Direction::DOWN => y += 1,
		Direction::LEFT => {
			if x == 0 {
				return None
			}
			x -= 1},
		Direction::RIGHT => x += 1,		
		_ => {}
	}
	if y >= height_map.len() {
		return None
	}
	if x >= height_map[y].len() {
		return None
	}
	Some((x,y))
} 

fn get_tile(height_map : &Vec<Vec<u32>>, (x, y) : (usize, usize), dir : Direction) -> Option<u32> {
	match get_tile_pos(height_map, (x,y), dir) {
		Some((z,w)) => Some(height_map[w][z]),
		_ => None
	}
} 

fn is_min_tile(height_map : &Vec<Vec<u32>>, (x,y) : (usize, usize)) -> bool {
	let val = get_tile(height_map, (x, y), Direction::NOP).unwrap();
	let up = get_tile(height_map, (x, y), Direction::UP);
	let down = get_tile(height_map, (x, y), Direction::DOWN);
	let left = get_tile(height_map, (x, y), Direction::LEFT);
	let right = get_tile(height_map, (x, y), Direction::RIGHT);

	for cell in [up,down,left,right] {
		match cell {
			Some(x) => if x <= val {
				return false
			}
			_ => {} 
		}
	}

	true
}

fn get_mins(height_map : &Vec<Vec<u32>>) -> Vec<(usize,usize)> {
	let mut mins : Vec<(usize,usize)> = Vec::new();

	for y in 0..height_map.len() {
		for x in 0..height_map[y].len() {
			if is_min_tile(&height_map, (x, y)){
				mins.push((x,y));
			}
		}
	}

	mins
}

pub fn day9_2(height_map : &Vec<Vec<u32>>) -> usize {
	let mins = get_mins(height_map); 
	let mut basins : Vec<usize> = Vec::new();

	let mut visited : HashSet<(usize, usize)> = HashSet::new();
	for min in mins {
		basins.push(count_to_nine(&mut visited, height_map, min));
	}

	basins.sort();
	basins.reverse();
	
	basins[0] * basins[1] * basins[2]
}

const VISITABLE: &'static [Direction] = &[Direction::DOWN,Direction::UP,Direction::LEFT,Direction::RIGHT];

fn count_to_nine(visited : &mut HashSet<(usize, usize)>, height_map : &Vec<Vec<u32>>, (x,y) : (usize, usize)) -> usize {
	if visited.contains(&(x,y)) {
		return 0;
	}
	visited.insert((x,y));

	let tile = get_tile(height_map, (x,y), Direction::NOP).unwrap();
	if tile == 9 {
		return 0;
	}

	let mut sum = 1;
	
	for dir in VISITABLE {
		let pos = get_tile_pos(height_map, (x,y), *dir);
		match pos {
			Some(p) => {
				sum += count_to_nine(visited, height_map, p);
			}, 
			_ => {},
		}
	}

	sum
}


#[cfg(test)]
mod tests {
	use super::*;

	#[test]
	fn test9_1() {
		let input = &String::from("2199943210\n3987894921\n9856789892\n8767896789\n9899965678\n");
		let height_map = to_2d_vector(input);
		assert_eq!(15,day9_1(&height_map))
	}

	#[test]
	fn test9_2() {
		let input = &String::from("2199943210\n3987894921\n9856789892\n8767896789\n9899965678\n");
		let height_map = to_2d_vector(input);
		assert_eq!(1134,day9_2(&height_map))
	}

}