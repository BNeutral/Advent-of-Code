use std::collections::HashSet;

#[allow(dead_code)]
pub fn day4(input : &String) -> () {
	let data = parse(input);
	println!("Part1: {}", day4_1(&data));
	println!("Part2: {}", day4_2(&data));
}

pub fn day4_1(input : &BingoData) -> i32 {
	input.roll_numbers(true)
}

pub fn day4_2(input : &BingoData) -> i32 {
	input.roll_numbers(false)
}

#[derive(Copy, Clone, Debug, Hash)]
pub struct BingoNUmber {
	number : i32,
	marked : bool
}

#[derive(Copy, Clone, Debug, Hash)]
pub struct BingoCard {
	data : [[BingoNUmber;5];5],
}

#[derive(Debug)]
pub struct BingoData {
	rolled_numbers : Vec<i32>,
	cards : Vec<BingoCard>
}

impl BingoData {
	fn roll_numbers(&self, call_first : bool) -> i32 {
		let mut clone = self.cards.clone(); // To avoid ownership problems and also not affect other functions calls to this
		let mut winners = HashSet::new();
		for rolled in &self.rolled_numbers {
			let mut count = 0;
			for card in clone.iter_mut() {
				if card.mark_number(*rolled) {
					if call_first {
						return card.sum_unmarked() * rolled;
					} else {
						winners.insert(count);
					}
					if winners.len() == self.cards.len(){
						return card.sum_unmarked() * rolled;
					}
				}
				count += 1;
			}
		}
		-1
	}
}

impl BingoCard {
	fn mark_number(&mut self, num : i32) -> bool {
		for y in 0..5 {
			for x in 0..5 {
				let mut cell = &mut self.data[y][x];
				if cell.number == num {
					cell.marked = true;	
					if self.check_bingo() {
						return true;
					}
				}
			}
		}
		false
	}

	fn check_bingo(&self) -> bool {
		for y in 0..5 {
			let mut mark = true;
			for x in 0..5 {
				let cell = self.data[y][x];
				mark = mark && cell.marked;
			}
			if mark { 
				return true;
			}
		}
		for x in 0..5 {
			let mut mark = true;
			for y in 0..5 {
				let cell = self.data[y][x];
				mark = mark && cell.marked;
			}
			if mark { 
				return true;
			}
		}
		false
	}

	fn sum_unmarked(&self) -> i32 {
		let mut result = 0;
		for y in 0..5 {
			for x in 0..5 {
				let cell = self.data[y][x];
				if !cell.marked {
					result += cell.number;
				}
			}
		}
		result
	}
}

fn parse(input : &String) -> BingoData{
	let mut got_first_line = false;
	let mut card_line_counter = 0;

	let mut data = BingoData {
		rolled_numbers : Vec::new(),
		cards : Vec::new()
	};

	for line in input.lines() {
		if !got_first_line {
			for number in line.split(',') {
				data.rolled_numbers.push(number.parse::<i32>().unwrap());
			}
			got_first_line = true;
			continue;
		}

		if line.is_empty() {
			card_line_counter = 0;
			data.cards.push(BingoCard {
				data : [[BingoNUmber{ number: 0, marked : false};5];5]	
			});
		} else {
			let mut index = 0;
			let mut card = data.cards.last_mut().unwrap();
			for num in line.split_whitespace() {
				let parsed_num = num.parse::<i32>().unwrap();
				card.data[card_line_counter][index].number = parsed_num;
				index += 1;
			}
			card_line_counter += 1;	
		}
	}

	data
}

#[cfg(test)]
mod tests {
	use super::*;

	#[test]
	fn test4_1() {
		let input = &String::from("7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1\n\n22 13 17 11  0\n 8  2 23  4 24\n21  9 14 16  7\n 6 10  3 18  5\n 1 12 20 15 19\n\n 3 15  0  2 22\n 9 18 13 17  5\n19  8  7 25 23\n20 11 10 24  4\n14 21 16 12  6\n\n14 21 17 24  4\n10 16 15  9 19\n18  8 23 26 20\n22 11 13  6  5\n 2  0 12  3  7");
		let data = parse(input);
		assert_eq!(4512,day4_1(&data))
	}

	
	#[test]
	fn test4_2() {
		let input = &String::from("7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1\n\n22 13 17 11  0\n 8  2 23  4 24\n21  9 14 16  7\n 6 10  3 18  5\n 1 12 20 15 19\n\n 3 15  0  2 22\n 9 18 13 17  5\n19  8  7 25 23\n20 11 10 24  4\n14 21 16 12  6\n\n14 21 17 24  4\n10 16 15  9 19\n18  8 23 26 20\n22 11 13  6  5\n 2  0 12  3  7");
		let data = parse(input);
		assert_eq!(1924,day4_2(&data))
	}
}