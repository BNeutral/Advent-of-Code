use std::collections::HashMap;
use regex::Regex;

#[allow(dead_code)]
pub fn day21(input : &String) -> () {
	println!("Part1: {}", day21_1(input));
	println!("Part2: {}", day21_2(input));
}

pub fn day21_1(input : &String) -> u64 {
	let mut game : GameState = GameState::from(input);

	let mut die = DeterministicDie::new();

	loop {
		let player : &mut Player = game.get_current_player();
		let mut sum = 0;
		for _ in 0..3 {
			sum += die.roll();
		}
		player.advance(sum);
		if player.score >= 1000 {
			game.switch_player();
			let player = game.get_current_player();
			return (player.score as u64) * (die.roll_counter as u64);
		}
		game.switch_player();
	}
}

pub fn day21_2(input : &String) -> u64 {
	let game : GameState = GameState::from(input);

	// roll -> times it's present in all possib
	let mut roll_probability : HashMap<u16, u64> = HashMap::new();
	for a in 1..4{
		for b in 1..4 {
			for c in 1..4 {
				*roll_probability.entry(a+b+c).or_insert(0) += 1
			}
		}
	}

	// gamestate -> wins
	let mut known_branches : HashMap<GameState, (u64, u64)> = HashMap::new();

	let wins = recursive_part2(game, &roll_probability, &mut known_branches);

	std::cmp::max(wins.0, wins.1)
}

fn recursive_part2(game : GameState, roll_probability : &HashMap<u16, u64>, known_branches : &mut HashMap<GameState, (u64, u64)>) -> (u64, u64) {
	match known_branches.get(&game) {
		Some(val) => { return *val }
		_ => {}
	};

	if game.player1.score >= 21 {
		return (1,0)
	}
	if game.player2.score >= 21 {
		return (0,1)
	}

	let mut w1 = 0;
	let mut w2 = 0;
	for entry in roll_probability {
		let mut new_game = game.clone();
		let rolled = entry.0;
		let mult = entry.1;
		new_game.get_current_player().advance(*rolled);
		new_game.switch_player();
		let result = recursive_part2(new_game, &roll_probability, known_branches);
		known_branches.insert(new_game, result);
		w1 += mult * result.0;
		w2 += mult * result.1;
	}

	known_branches.insert(game, (w1, w2));
	return (w1, w2);
}

pub struct DeterministicDie {
	roll_counter : u16,
}

impl DeterministicDie {
	fn new() -> DeterministicDie {
		DeterministicDie {
			roll_counter : 0, 
		}
	}

	fn roll(&mut self) -> u16 {
		let result : u16 = 1 + self.roll_counter % 100;
		self.roll_counter += 1;
		result
	}

}

#[derive(Debug, Copy, Clone, Eq, PartialEq, Hash)]
struct GameState {
	player1: Player,
	player2: Player,
	current_player: u8
}

impl GameState {
	pub fn from(input : &str) -> GameState {
		let mut players : Vec<Player> = Vec::new(); 
		for line in input.lines() {
			players.push(Player::from(line));
		}
		GameState {
			player1 : players[0],
			player2 : players[1],
			current_player : 0
		}
	}

	pub fn get_current_player(&mut self) -> &mut Player {
		if self.current_player == 0 {
			&mut self.player1
		}
		else {
			&mut self.player2
		}
	}

	pub fn switch_player(&mut self) {
		match self.current_player {
			0 => self.current_player = 1,
			1 => self.current_player = 0,
			_ => panic!("Wrong players")
		}
	}
}

#[derive(Debug, Copy, Clone, Eq, PartialEq, Hash)]
struct Player {
	position : u16,
	score: u16,
}

impl Player {
	pub fn from(input : &str) -> Player {
		let reg = Regex::new(r"Player (\d+) starting position: (\d+)").unwrap();
		let captures = reg.captures(input).unwrap();

		Player {
			position: captures.get(2).unwrap().as_str().parse().unwrap(),
			score: 0
		}
	}

	pub fn advance(&mut self, dice_sum : u16) {
		self.position = (dice_sum + (self.position - 1) ) % 10 + 1;
		self.score += self.position;
	}
}

#[cfg(test)]
mod tests {
	use super::*;
	
	#[test]
	fn test21_1() {
		let input = String::from("Player 1 starting position: 4\nPlayer 2 starting position: 8\n");
		assert_eq!(739785, day21_1(&input));
	}

	#[test]
	fn test21_2() {
		let input = String::from("Player 1 starting position: 4\nPlayer 2 starting position: 8\n");
		assert_eq!(444356092776315, day21_2(&input));
	}
}