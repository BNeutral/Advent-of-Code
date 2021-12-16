use std::fmt;

#[allow(dead_code)]
pub fn day16(input : &String) -> () {
	println!("Part1: {}", day16_1(input));
	println!("Part2: {}", day16_2(input));
}

pub fn day16_1(input : &String) -> u64 {
	let bit_vec = BitVec::new(input);
	bit_vec.sum_version_numbers()
}

pub fn day16_2(input : &String) -> u64 {
	let bit_vec = BitVec::new(input);
	bit_vec.calculate()
}

#[derive(Debug)]
struct BitVec {
	vec : Vec<u8> 
}

impl BitVec {
	pub fn new(input : &String) -> BitVec {
		let trimmed = input.trim();
		if (trimmed.len() % 2) != 0 {
			panic!("Trying to parse half bytes");
		} 

		let bit_vec = BitVec {
			vec : hex::decode(trimmed).unwrap()
		};

		bit_vec
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

	pub fn get_number_until_end(&self, start : usize) -> (u64, usize) {
		let mut keep_reading = true;
		let mut idx = start;
		let mut half_bytes : Vec<u8> = Vec::new();

		while keep_reading {
			keep_reading = self.get_bit(idx) == 1;
			idx += 1;
			half_bytes.push(self.get_bits(idx, 4) as u8);
			idx += 4;
		}

		let mut res : u64 = 0;
		let len = half_bytes.len();
		for x in 0..len {
			res |= (half_bytes[x] as u64) << (len-1-x) * 4;
		}

		(res, idx-start)
	}

	pub fn get_number_until_end_and_advance(&self, start : &mut usize) -> u64 {
		let (result, advanced) = self.get_number_until_end(*start);
		*start += advanced;
		result
	}

	pub fn sum_version_numbers(&self) -> u64 {
		self.parse_packet(0).0
	}

	pub fn calculate(&self) -> u64 {
		self.parse_packet(0).2
	}

	pub fn parse_packet(&self, start : usize) -> (u64, usize, u64) {
		let mut idx = start;
		let version = self.get_bits_and_advance(&mut idx, 3);
		let id = self.get_bits_and_advance(&mut idx, 3);

		let mut version_sum = version;
		let val : u64;

		match id {
			4 => { // literal
				val = self.get_number_until_end_and_advance(&mut idx);
			}
			op => { // operator
				let mut sub_vals : Vec<u64> = Vec::new();
				match self.get_bit_and_advance(&mut idx) { // length id
					0 => {
						let sub_packet_len = self.get_bits_and_advance(&mut idx, 15) as usize;
						let sub_start = idx;
						while idx < sub_start+sub_packet_len {
							let (v_sum, read, sub_val) = self.parse_packet(idx);
							version_sum += v_sum;
							idx += read; 
							sub_vals.push(sub_val);
						}
					},
					1 => {
						let subpacket_count = self.get_bits_and_advance(&mut idx, 11);
						for _x in 0..subpacket_count {
							let (v_sum, read, sub_val) = self.parse_packet(idx);
							version_sum += v_sum;
							idx += read; 
							sub_vals.push(sub_val);
						}
					}
					_ => panic!("Somehow you fetched a bit but got something else!")
				}
				match op {
					0 => val = sub_vals.iter().sum(),
					1 => val = sub_vals.iter().product(),
					2 => val = *sub_vals.iter().min().unwrap(),
					3 => val = *sub_vals.iter().max().unwrap(),
					4 => if sub_vals[0] > sub_vals[1]{
						val = 1;
					} else {
						val = 0
					},
					5 => if sub_vals[0] > sub_vals[1]{
						val = 1;
					} else {
						val = 0
					}
					6 => if sub_vals[0] < sub_vals[1]{
						val = 1;
					} else {
						val = 0
					}
					7 => if sub_vals[0] == sub_vals[1]{
						val = 1;
					} else {
						val = 0
					}
					_ => panic!("Unsuported op")
				}
			} 
		}

		let read_bits = idx - start;
		(version_sum, read_bits, val)
	}
}

impl fmt::Display for BitVec {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
		let mut res = Ok(());
		for byte in self.vec.iter() {
			res = write!(f, "{:b}", byte);
			match res {
				Ok(_) => {},
				Err(_) => return res
			}
		}
		res
    }
}

#[cfg(test)]
mod tests {
	use super::*;

	#[test]
	fn test16_parse() {
		let bit_vec = BitVec::new(&String::from("D2FE28"));
		println!("{}",bit_vec);
		assert_eq!(6,bit_vec.get_bits(0, 3));
		assert_eq!(4,bit_vec.get_bits(3, 3));
		assert_eq!(1,bit_vec.get_bit(6));
		assert_eq!(7,bit_vec.get_bits(7, 4));
		assert_eq!(1,bit_vec.get_bit(11));
		assert_eq!(14,bit_vec.get_bits(12, 4));
		assert_eq!(0,bit_vec.get_bit(16));
		assert_eq!(5,bit_vec.get_bits(17, 4));
		assert_eq!(2021,bit_vec.get_number_until_end(6).0);
	} 

	#[test]
	fn test16_1_0() {
		let input = &String::from("EE00D40C823060");
		assert_eq!(14,day16_1(input));
	}

	#[test]
	fn test16_1_1() {
		let input = &String::from("8A004A801A8002F478");
		assert_eq!(16,day16_1(input));
	}

	#[test]
	fn test16_1_2() {
		let input = &String::from("620080001611562C8802118E34");
		assert_eq!(12,day16_1(input));
	}

	#[test]
	fn test16_1_3() {
		let input = &String::from("C0015000016115A2E0802F182340");
		assert_eq!(23,day16_1(input));
	}

	#[test]
	fn test16_1_4() {
		let input = &String::from("A0016C880162017C3686B18A3D4780");
		assert_eq!(31,day16_1(input));
	}

	#[test]
	fn test16_2_0() {
		let input = &String::from("C200B40A82");
		assert_eq!(3,day16_2(input));
	}

	#[test]
	fn test16_2_1() {
		let input = &String::from("04005AC33890");
		assert_eq!(54,day16_2(input));
	}

	#[test]
	fn test16_2_3() {
		let input = &String::from("880086C3E88112");
		assert_eq!(7,day16_2(input));
	}

	#[test]
	fn test16_2_4() {
		let input = &String::from("CE00C43D881120");
		assert_eq!(9,day16_2(input));
	}

	#[test]
	fn test16_2_5() {
		let input = &String::from("D8005AC2A8F0");
		assert_eq!(1,day16_2(input));
	}

	#[test]
	fn test16_2_6() {
		let input = &String::from("9C005AC2F8F0");
		assert_eq!(0,day16_2(input));
	}

	#[test]
	fn test16_2_7() {
		let input = &String::from("9C0141080250320F1802104A08");
		assert_eq!(1,day16_2(input));
	}
}