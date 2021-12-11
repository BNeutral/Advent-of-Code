use std::collections::HashMap;

#[allow(dead_code)]
pub fn day10(input : &String) -> () {
	let (d1, d2) =  solve(&input);
	println!("Part1: {}", d1);
	println!("Part2: {}", d2);
}

pub fn solve(input : &String) -> (i32, u64) {
	let openers : [char; 4] = ['(','[','{','<'];
	let closers : [char; 4] = [')',']','}','>'];
	let error_scores : [i32; 4] = [3,57,1197,25137];

	let mut close_match : HashMap<char,char> = HashMap::new();
	close_match.insert('(',')');
	close_match.insert('[',']');
	close_match.insert('{','}');
	close_match.insert('<','>');

	let mut incomplete_scores : HashMap<char,u64> = HashMap::new();
	incomplete_scores.insert('(',1);
	incomplete_scores.insert('[',2);
	incomplete_scores.insert('{',3);
	incomplete_scores.insert('<',4);

	let mut error_score = 0;
	let mut incomplete_line_score : Vec<u64> = Vec::new();

	for line in input.lines() {
		let mut error = false;
		let mut stack : Vec<char> = Vec::new(); 

		for ch in line.chars() {	
			for x in 0..4 {
				if openers[x] == ch {
					stack.push(ch);
				}
				if closers[x] == ch {
					let found = stack.pop().unwrap();
					let matching = close_match.get(&found).unwrap();
					if *matching != ch {
						error = true;
						error_score += error_scores[x];
						break;
					}
				}
			}
			if error {
				break;
			}
		}

		if !error { // Fix the good line
			let mut line_score : u64 = 0;
			while !stack.is_empty() {
				let ch = stack.pop().unwrap();
				let to_sum = incomplete_scores.get(&ch).unwrap();
				line_score = line_score * 5 + to_sum
			}
			incomplete_line_score.push(line_score);
		}
	}

	incomplete_line_score.sort();
	let incomplete_score = incomplete_line_score[incomplete_line_score.len() / 2];

	(error_score, incomplete_score)
}

#[cfg(test)]
mod tests {
	use super::*;

	#[test]
	fn test10_1() {
		let input = &String::from("[({(<(())[]>[[{[]{<()<>>\n[(()[<>])]({[<{<<[]>>(\n{([(<{}[<>[]}>{[]{[(<()>\n(((({<>}<{<{<>}{[]{[]{}\n[[<[([]))<([[{}[[()]]]\n[{[{({}]{}}([{[{{{}}([]\n{<[[]]>}<{[{[{[]{()[[[]\n[<(<(<(<{}))><([]([]()\n<{([([[(<>()){}]>(<<{{\n<{([{{}}[<[[[<>{}]]]>[]]\n");
		let (d1, _) = solve(&input);
		assert_eq!(26397,d1);
	}

	#[test]
	fn test10_2() {
		let input = &String::from("[({(<(())[]>[[{[]{<()<>>\n[(()[<>])]({[<{<<[]>>(\n{([(<{}[<>[]}>{[]{[(<()>\n(((({<>}<{<{<>}{[]{[]{}\n[[<[([]))<([[{}[[()]]]\n[{[{({}]{}}([{[{{{}}([]\n{<[[]]>}<{[{[{[]{()[[[]\n[<(<(<(<{}))><([]([]()\n<{([([[(<>()){}]>(<<{{\n<{([{{}}[<[[[<>{}]]]>[]]\n");
		let (_, d2) = solve(&input);
		assert_eq!(288957,d2);
	}

}