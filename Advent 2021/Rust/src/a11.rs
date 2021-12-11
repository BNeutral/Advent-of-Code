#[allow(dead_code)]
pub fn day11(input : &String) -> () {
	println!("Part1: {}", day11_1(input));
	println!("Part2: {}", day11_2(input));
}

pub fn day11_1(input : &String) -> u64 {
	let mut grid = OctoGrid::new(input);
	grid.simulate(100, false)
}

pub fn day11_2(input : &String) -> u64 {
	let mut grid = OctoGrid::new(input);
	grid.simulate(100, true)
}

const GRID_SIZE : usize = 10;

#[derive(Debug)]
pub struct OctoGrid {
	grid : [[i32;GRID_SIZE];GRID_SIZE],
	flashed : [[bool;GRID_SIZE];GRID_SIZE]
}

impl OctoGrid {
	pub fn new(input : &String) -> OctoGrid {
		let mut grid = OctoGrid {
			grid : [[0;GRID_SIZE];GRID_SIZE],
			flashed : [[false;GRID_SIZE];GRID_SIZE],
		};

		let mut y = 0;	
		for line in input.lines() {
			let mut x = 0;
			for ch in line.chars() {
				grid.grid[y][x] = ch.to_digit(10).unwrap() as i32;
				x += 1;
			}
			y +=1 ;
		}

		grid
	}

	pub fn simulate(&mut self, steps : i32, return_on_sync : bool) -> u64{
		let mut flash_counter = 0;

		if return_on_sync {
			let mut step = 0;
			loop {
				let flashed = self.step();
				step += 1;
				if flashed == (GRID_SIZE*GRID_SIZE) as u64 {
					return step as u64;
				}
			}
		} else {
			for _ in 0..steps {
				flash_counter += self.step()
			}
		}
		flash_counter
	}

	fn step(&mut self) -> u64 {
		self.increase_energy_all();
		//self.reset_flashed();
		self.flash_all()
	}

	fn increase_energy_all(&mut self) {
		for y in 0..GRID_SIZE {
			for x in 0..GRID_SIZE {
				self.grid[y][x] += 1;
			}
		}
	}

	fn flash_all(&mut self) -> u64 {
		let mut flash_counter = 0;
		let mut to_flash : Vec<(usize, usize)> = Vec::new();

		for y in 0..GRID_SIZE {
			for x in 0..GRID_SIZE {
				if self.grid[y][x] > 9 {
					to_flash.push((x,y));
					self.flashed[y][x] = true;
				}
			}
		}

		while !to_flash.is_empty() {
			let (x,y) = to_flash.pop().unwrap();
			
			flash_counter += 1;
			//println!("flashing {},{}",y,x);
			for (nx,ny) in self.get_valid_adjacents((x,y)) {
				self.grid[ny][nx] += 1;
				if self.grid[ny][nx] > 9 && !self.flashed[ny][nx] {
					to_flash.push((nx,ny));
					self.flashed[ny][nx] = true;
					//println!("adding {},{}", nx, ny);
				}
			}
		}

		for y in 0..GRID_SIZE {
			for x in 0..GRID_SIZE {
				if self.flashed[y][x] == true {
					self.grid[y][x] = 0;
					self.flashed[y][x] = false;
				}
			}
		}

		flash_counter
	}

	fn get_valid_adjacents(&mut self, (x,y) : (usize,usize)) -> Vec<(usize, usize)>{
		let mut adjacents : Vec<(usize, usize)> = Vec::new();
		for dy in -1..2 {
			for dx in -1..2 {
				if dx == 0 && dy == 0 {
					continue;
				}
				match self.get_tile_pos((x,y),(dx,dy)) {
					Some(p) => adjacents.push(p),
					_ => {}
				}
			}
		}
		adjacents
	}

	fn get_tile_pos(&mut self, (x, y) : (usize, usize), (deltax, deltay) : (i32, i32)) -> Option<(usize,usize)> {
		let newx = x as i32 + deltax;
		let newy = y as i32 + deltay;
		if newy < 0 || newy >= GRID_SIZE as i32 {
			return None
		}
		if newx < 0 || newx >= GRID_SIZE as i32 {
			return None
		}
		Some((newx as usize, newy as usize))
	} 
}

#[cfg(test)]
mod tests {
	use super::*;

	#[test]
	fn test_grid_adj() {
		let mut grid = OctoGrid {
			grid : [[0;GRID_SIZE];GRID_SIZE],
			flashed : [[false;GRID_SIZE];GRID_SIZE],
		};
		let adj = grid.get_valid_adjacents((5,5));
		assert_eq!(adj.contains( &(4,4) ) , true);
		assert_eq!(adj.contains( &(4,5) ) , true);
		assert_eq!(adj.contains( &(4,6) ) , true);
		assert_eq!(adj.contains( &(5,4) ) , true);
		assert_eq!(adj.contains( &(5,6) ) , true);
		assert_eq!(adj.contains( &(6,4) ) , true);
		assert_eq!(adj.contains( &(6,5) ) , true);
		assert_eq!(adj.contains( &(6,6) ) , true);
		assert_eq!(adj.len(), 8);
	}

	#[test]
	fn test11_1() {
		let input = &String::from("5483143223\n2745854711\n5264556173\n6141336146\n6357385478\n4167524645\n2176841721\n6882881134\n4846848554\n5283751526\n");
		assert_eq!(1656,day11_1(input));
	}


	#[test]
	fn test11_2() {
		let input = &String::from("5483143223\n2745854711\n5264556173\n6141336146\n6357385478\n4167524645\n2176841721\n6882881134\n4846848554\n5283751526\n");
		assert_eq!(195,day11_2(input));
	}

}