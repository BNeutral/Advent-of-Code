use std::collections::HashSet;
use std::fmt;

#[allow(dead_code)]
pub fn day23(input : &String) -> () {
	println!("Part1: {}", day23_1(input));
	println!("Part2: {}", day23_2(input));
}

pub fn day23_1(input : &String) -> usize {
	let initial_state = State::new(input);
	initial_state.solve()
}

pub fn day23_2(input : &String) -> usize {
	let mut input_edited : String = String::new();

	let mut counter = 0;
	for line in input.lines() {
		if counter == 3 {
			input_edited += "  #D#C#B#A#  \n  #D#B#A#C#  \n";
		}
		input_edited += line; 
		input_edited += "\n";
		counter += 1;
	}

	let initial_state = State::new(&input_edited);

	initial_state.solve()
}

pub fn energy_req(ch : char) -> usize  {
	match ch {
		'A' => 1, 'B' => 10, 'C' => 100, 'D' => 1000,
		_ => panic!("Not an amphipod type")
	}
}

pub fn dest_side(ch : char) -> usize  {
	match ch {
		'A' => 0, 'B' => 1, 'C' => 2, 'D' => 3,
		_ => panic!("Not an amphipod type")
	}
}

static SIDE_POS : [usize; 4] = [2,4,6,8];
static VALID_HALL : [usize; 7] = [0,1,3,5,7,9,10];
static CLOSEST_VALID_HALL : [[usize; 7];4] = [
	[3,1,5,0,7,9,10],
	[5,3,7,1,9,0,10],
	[5,7,3,9,1,10,0],
	[7,9,5,10,3,1,0]
];


#[derive(Debug, Clone, Eq, PartialEq, Hash)]
struct State {
	hallway : [char; 11],
	sides : Vec<Vec<char>>,
	energy_used : usize,
	non_empty : Vec<bool>,
	solved : Vec<bool>,
}

impl State {
	pub fn new(input : &String) -> State{
		let mut state = State {
			hallway : ['.';11],
			sides : vec![Vec::new();4],
			energy_used : 0,
			non_empty : vec![true;4],
			solved : vec![false;4],
		};
	
		let mut line_counter = 0;
		for line in input.lines() {
			if line_counter >= 2 {
				let mut ch_counter = 0;
				for ch in line.chars() {
					if ch.is_alphabetic() {
						state.sides[ch_counter].push(ch);
						ch_counter += 1;
					}
				}
			}
			line_counter += 1;
		} 

		state
	}

	pub fn try_move_out(&mut self, side_idx : usize, target_pos : usize) -> bool {
		let start_pos = SIDE_POS[side_idx];
		if !self.can_walk_to(start_pos, target_pos) {
			return false;
		}

		let side = &mut self.sides[side_idx];
		
		for i in 0..side.len() {
			let amphi = side[i];
			if amphi != '.' {
				self.hallway[target_pos] = amphi;
				side[i] = '.';
				if i == side.len() -1 {
					self.non_empty[side_idx] = false;
				} 
				self.energy_used += self.walk_energy(amphi, start_pos, target_pos) + (i+1) * energy_req(amphi);				
				return true;
			}
		}
		
		return false;
	}

	pub fn try_move_in(&mut self, start_pos : usize) -> bool {
		let amphi = self.hallway[start_pos];
		let side_idx = dest_side(amphi);
		let dst = SIDE_POS[side_idx];

		if !self.can_walk_to(start_pos, dst) {
			return false;
		}

		let side = &mut self.sides[side_idx];
		for in_idx in (0..side.len()).rev() {
			if side[in_idx] == '.' {
				side[in_idx] = amphi;
				let dst = SIDE_POS[side_idx];
				self.hallway[start_pos] = '.';
				self.energy_used += self.walk_energy(amphi, start_pos, dst) + (in_idx+1) * energy_req(amphi);
				if in_idx == 0 {
					self.solved[side_idx] = true;
				}
				return true;
			}
			else if side[in_idx] == amphi {
				continue;
			} else {
				return false;
			}
		}

		return false;
	}

	pub fn walk_energy(&self, amphi : char, from_idx : usize, to_idx : usize) -> usize {
		let start = std::cmp::min(from_idx, to_idx);
		let end = std::cmp::max(from_idx, to_idx);
		(end - start) * energy_req(amphi)
	}

	pub fn can_walk_to(&self, from_idx : usize, to_idx : usize) -> bool {
		let start = std::cmp::min(from_idx, to_idx);
		let end = std::cmp::max(from_idx, to_idx);		
		for x in start..end+1 {
			if x == from_idx {
				continue;
			}
			if self.hallway[x] != '.' {
				return false;
			}
		}
		true
	} 

	pub fn is_solved(&self) -> bool  {
		for i in 0..4 {
			if !self.is_solved_side(i) {
				return false
			}
		}
		true
	}

	pub fn is_solved_side(&self, side_idx : usize) -> bool  {
		self.solved[side_idx]
	}
	
	pub fn solve(&self) -> usize {
		let mut best = usize::MAX;
		let mut known_states : HashSet<State> = HashSet::new();
		self.sub_solve(&mut best, &mut known_states);
		best
	}

	pub fn sub_solve(&self, best_so_far : &mut usize, known_states : &mut HashSet<State>) {
		if self.energy_used >= *best_so_far || known_states.contains(self) {
			return;
		}

		if self.is_solved() {
			*best_so_far = std::cmp::min(self.energy_used, *best_so_far);
			return;
		}

		for x in VALID_HALL {
			if self.hallway[x] != '.' {
				let mut new = self.clone();
				if new.try_move_in(x) {
					new.sub_solve(best_so_far, known_states);
					known_states.insert(new);
				}
			}
		}

		for idx in 0..4 {
			if self.non_empty[idx] == true {
				for i in CLOSEST_VALID_HALL[idx] {
					if self.hallway[i] == '.' {
						let mut new = self.clone();
						if new.try_move_out(idx, i) {
							new.sub_solve(best_so_far, known_states);
							known_states.insert(new);
						}
					}
				}
			}
		}	
	}
}

impl fmt::Display for State {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
		// TODO: Write errors
		write!(f, "#############\n")?;
		write!(f, "#")?;
		for ch in self.hallway {
			write!(f, "{}", ch)?;
		}
		write!(f, "#\n")?;
		write!(f, "###{}#{}#{}#{}###\n", self.sides[0][0], self.sides[1][0], self.sides[2][0], self.sides[3][0])?;
		for x in 1..self.sides[0].len() {
			write!(f, "  #{}#{}#{}#{}#  \n", self.sides[0][x], self.sides[1][x], self.sides[2][x], self.sides[3][x])?;
		}
		write!(f, "  #########  ")?;

		fmt::Result::Ok(())
    }
}

#[cfg(test)]
mod tests {
	use super::*;

	#[test]
	fn test23_0() {
		let input = String::from("#############\n#...........#\n###B#C#B#D###\n  #A#D#C#A#\n  #########\n");
		let mut state = State::new(&input);
		state.try_move_out(2, 3);
		assert_eq!(40, state.energy_used);
		state.try_move_out(1, 5);
		assert_eq!(240, state.energy_used);
		assert_eq!(false, state.try_move_in(3));
		state.try_move_in(5);
		assert_eq!(440, state.energy_used);
		state.try_move_out(1, 5);
		assert_eq!(3440, state.energy_used);
		state.try_move_in(3);
		assert_eq!(3470, state.energy_used);
		state.try_move_out(0, 3);
		state.try_move_in(3);
		assert_eq!(3510, state.energy_used);

		state.try_move_out(3, 7);
		state.try_move_out(3, 9);
		assert_eq!(5513, state.energy_used);

		state.try_move_in(7);
		state.try_move_in(5);
		state.try_move_in(9);
		assert_eq!(12521, state.energy_used);
	}

	// Because rust tests are run in threads with smaller stack size, these overflow, so I've commented them out	
	/*#[test]
	fn test23_1() {
		let input = String::from("#############\n#...........#\n###B#C#B#D###\n  #A#D#C#A#\n  #########\n");
		assert_eq!(12521, day23_1(&input));
	}

	#[test]
	fn test23_2() {
		let input = String::from("#############\n#...........#\n###B#C#B#D###\n  #A#D#C#A#\n  #########\n");
		assert_eq!(44169, day23_2(&input));
	}*/
}