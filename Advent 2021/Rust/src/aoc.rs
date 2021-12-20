use std::fmt;

#[allow(dead_code)]
pub fn to_vector(input : &str) -> Vec<i32> {
	let mut res = Vec::new();
	for line in input.lines() {
		res.push(line.parse::<i32>().unwrap());
	}
	res
}

#[allow(dead_code)]
pub fn to_2d_vector(input : &str) -> Vec<Vec<u32>> {
	let mut res = Vec::new();
	for line in input.lines() {
		let mut tiles = Vec::new();
		for ch in line.trim().chars() {
			tiles.push(ch.to_digit(10).unwrap());
		}
		res.push(tiles);
	}
	res
}

#[allow(dead_code)]
pub fn to_char_vec(input : &str) -> Vec<Vec<char>> {
	let mut res = Vec::new();
	for line in input.lines() {
		res.push(line.chars().collect());
	}
	res
}

pub fn is_lowercase(string : &String) -> bool {
	string.chars().all(|c| c.is_ascii_lowercase())
}

#[derive(Debug)]
pub struct BitVec {
	pub vec : Vec<u8> 
}

#[allow(dead_code)]
impl BitVec {
	pub fn new() -> BitVec {
		BitVec {
			vec : Vec::new(),
		}
	}

	pub fn new_sized(bits : usize) -> BitVec {
		let mut bytes = bits / 8;
		if bits % 8 != 0 {
			bytes += 1;
		}
		BitVec {
			vec : vec![0;bytes],
		}
	}

	pub fn set_bit(&mut self, index : usize) {
		let pos = index / 8;
		if self.vec.len() <= pos {
			self.vec.resize(pos+1, 0);
		}

		let offset = (7 - index % 8) as u8;
		self.vec[pos] |= 1 << offset;
	}

	pub fn get_bit(&self, index : usize) -> u8 {
		let pos = index / 8;
		let offset = 7 - index % 8;
		let byte = self.vec[pos];	
		(byte >> offset) & 1
	}

	pub fn get_bits(&self, start : usize, len : usize) -> u64 {
		let mut result : u64 = 0;
		for x in 0..len {
			result |= (self.get_bit(start+x) as u64) << (len-x-1);
		}
		result
	}
	
	pub fn get_bit_and_advance(&self, start : &mut usize) -> u8 {
		let res = self.get_bit(*start);
		*start += 1;
		res
	}

	pub fn get_bits_and_advance(&self, start : &mut usize, len : usize) -> u64 {
		let res = self.get_bits(*start, len);
		*start += len;
		res
	}
}

impl fmt::Display for BitVec {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
		let mut res : fmt::Result = fmt::Result::Ok(());
		for entry in self.vec.iter() {
			res = write!(f, "{:08b}", entry);
			match res {
				fmt::Result::Err(_) => return res,
				_ => {}
			}
		}
		res
    }
}