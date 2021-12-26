#[allow(dead_code)]
pub fn day25(input : &String) -> () {
	println!("Part1: {}", day25_1(input));
}

pub fn day25_1(input : &String) -> usize {
	let mut map : Vec<Vec<char>> = Vec::new();

	for line in input.lines() {
		map.push(Vec::new());
		for ch in line.chars() {
			map.last_mut().unwrap().push(ch);
		}
	}

	let width = map[0].len();
	let height = map.len();
	let mut moves = 1;
	let mut counter = 0;
	while moves != 0 {
		//println!("Step {}", counter);
		//print_map(&map);
		match step(map, height, width) {
			(x,y) => {
				moves = x;
				map = y
			}
		}
		counter += 1;
	}

	counter
}

fn step(mut map: Vec<Vec<char>>, height : usize, width : usize) -> (usize, Vec<Vec<char>>) {
	let mut new = get_new_map(height, width);
	let mut moves = 0;

	for y in 0..height {
		for x in 0..width {
			if map[y][x] == 'v' {
				new[y][x] = 'v';
			}
			else if map[y][x] == '>'{
				if map[y][(x+1)%width] == '.' {
					moves += 1;
					new[y][(x+1)%width] = '>';
				} else {
					new[y][x] = '>';
				}
			}
		}
	}

	map = new;
	let mut new = get_new_map(height, width);
	for y in 0..height {
		for x in 0..width {
			if map[y][x] == '>' {
				new[y][x] = '>';
			}
			else if map[y][x] == 'v' {
				if map[(y+1)%height][x] == '.'  {
					moves += 1;
					new[(y+1)%height][x] = 'v';
				} else {
					new[y][x] = 'v';
				}
			}
			
		}
	}

	(moves, new)
}

fn get_new_map(height : usize, width : usize) -> Vec<Vec<char>> {
	let mut new : Vec<Vec<char>> = Vec::new();
	new.resize_with(height, || Vec::new());
	for y in 0..height {
		for _ in 0..width {
			new[y].resize_with(width, || '.');
		}
	}
	new
}

#[allow(dead_code)]
fn print_map(map: &Vec<Vec<char>>) {
	for y in 0..map.len() {
		for x in 0..map[y].len() {
			print!("{}",map[y][x]);
		}
		println!();
	}
}

#[cfg(test)]
mod tests {
	use super::*;

	#[test]
	fn test25() {
		let input = String::from("v...>>.vv>\n.vv>>.vv..\n>>.>v>...v\n>>v>>.>.v.\nv>v.vv.v..\n>.>>..v...\n.vv..>.>v.\nv.v..>>v.v\n....v..v.>\n");
		assert_eq!(1, day25_1(&input));
	}

}