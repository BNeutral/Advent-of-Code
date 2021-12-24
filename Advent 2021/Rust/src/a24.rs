#[allow(dead_code)]
pub fn day24(input : &String) -> () {
	//day24_test(input);
	println!("Part1: {}", day24_test(input, [9,9,4,2,9,7,9,5,9,9,3,9,2,9]));
	println!("Part2: {}", day24_test(input, [1,8,1,1,3,1,8,1,5,7,1,6,1,1]));
}

// Rules from input worked out by hand, see ../input/24_clean.txt for details

// i5 = i4 - 2
// i6 = i3 + 7
// i8 = i7 + 4
// i10 = i9 - 6
// i11 = i2 + 5
// i12 = i1 - 7 
// i0 = i1

pub fn day24_test(input: &String, nums : [i64;14]) -> String {
	let lines : Vec<&str> = input.lines().collect();
	let mut line_idx = 0;
	let mut registers = [0;4];

	// Part 1
			    //0 1 2 3 4 5 6 7 8 9 0 1 2 3 
	//let nums = [9,9,4,2,9,7,9,5,9,9,3,9,2,9]; 

	// Part 2
			  //0 1 2 3 4 5 6 7 8 9 0 1 2 3 
	// let nums = [1,8,1,1,3,1,8,1,5,7,1,6,1,1]; 
 
	let mut counter = 0; 
	while line_idx < lines.len() {
		let num = nums[counter];
		line_idx = execute(&mut registers, &lines, line_idx, vec![num], true);
		//println!("Registers {:?}\n", registers);
		counter += 1;
	}

	if registers[3] == 0 {
		return nums.iter().map( |&id| id.to_string()).collect(); 
	}
	String::from("Wrong num")
}

pub fn letter_to_idx(letter : &str) -> usize {
	match letter {
		"w" => 0, "x" => 1,	"y" => 2, "z" => 3,
		_ => panic!("Bad index")
	}
}

pub fn execute(registers: &mut  [i64;4], lines : &Vec<&str>, start_idx : usize, input_num : Vec<i64>,  stop_on_inp : bool) -> usize {
	let mut inp_counter = 0;

	for idx in start_idx..lines.len() {
		let line = lines[idx];
		let command : Vec<&str> = line.trim().split_ascii_whitespace().collect();

		let mut second_val = 0;
		if command.len() == 3 {
			if command[2] == "w" || command[2] == "x" || command[2] == "y" || command[2] == "z" { 
				second_val = registers[letter_to_idx(command[2])];
			} else {
				second_val = command[2].parse().unwrap();
			}
		}
		let first_idx = letter_to_idx(command[1]);

		match command[0] {
			"inp" => {
				if inp_counter > 0 && stop_on_inp {
					return idx
				}
				registers[first_idx] = input_num[inp_counter];
				inp_counter += 1;
			},
			"add" => {
				registers[first_idx] = registers[first_idx] + second_val;
			},
			"mul" => {
				registers[first_idx] = registers[first_idx] * second_val;
			},
			"div" => {
				registers[first_idx] = registers[first_idx] / second_val;
			},
			"mod" => {
				registers[first_idx] = registers[first_idx] % second_val;
			},
			"eql" => {
				if 	registers[first_idx] == second_val {
					registers[first_idx] = 1;
				} else {
					registers[first_idx] = 0;
				}
			},
			_ => { 
				panic!("Bad op {:?}", command);
			}
		}
	} 

	lines.len()
}

#[cfg(test)]
mod tests {
	use super::*;

	#[test]
	fn test24_p_1() {
		let input = String::from("inp x\nmul x -1");
		let lines : Vec<&str> = input.lines().collect();
		let mut registers = [0;4];
		execute(&mut registers, &lines, 0, vec![1], false);
		assert_eq!(-1, registers[1]);
	}

	#[test]
	fn test24_p_2() {
		let input = String::from("inp z\ninp x\nmul z 3\neql z x\n");
		let lines : Vec<&str> = input.lines().collect();
		let mut registers = [0;4];
		execute(&mut registers, &lines, 0, vec![1,3], false);
		assert_eq!(1, registers[3]);
		let mut registers = [0;4];
		execute(&mut registers, &lines, 0, vec![1,1], false);
		assert_eq!(0, registers[3]);
	}

	#[test]
	fn test24_p_3() {
		let input = String::from("inp w\nadd z w\nmod z 2\ndiv w 2\nadd y w\nmod y 2\ndiv w 2\nadd x w\nmod x 2\ndiv w 2\nmod w 2\n");
		let lines : Vec<&str> = input.lines().collect();
		let mut registers = [0;4];
		execute(&mut registers, &lines, 0, vec![255], false);
		assert_eq!(1, registers[3]);
		assert_eq!(1, registers[2]);
		assert_eq!(1, registers[1]);
		assert_eq!(1, registers[0]);

		let mut registers = [0;4];
		execute(&mut registers, &lines, 0, vec![1], false);
		assert_eq!(1, registers[3]);
		assert_eq!(0, registers[2]);
		assert_eq!(0, registers[1]);
		assert_eq!(0, registers[0]);
	}

}