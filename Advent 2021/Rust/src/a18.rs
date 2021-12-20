use std::fmt;

#[allow(dead_code)]
pub fn day18(input : &String) -> () {
	println!("Part1: {}", day18_1(input));
	println!("Part2: {}", day18_2(input));
}

pub fn day18_1(input : &String) -> u64 {
	let mut to_sum : Vec<SnailNumber> = Vec::new();
	for line in input.lines() {
		let mut number = SnailNumber::new(line);
		number.reduce();
		to_sum.push(number);
	}

	let result = SnailNumber::sum_consume(&mut to_sum);
	result.magnitude()
}

pub fn day18_2(input : &String) -> u64 {
	let mut best_magnitude = 0;

	let mut to_skip = 1;
	for line1 in input.lines() {
		let iter2 = input.lines().skip(to_skip);
		to_skip += 1;
		for line2 in iter2 {
			let n1_1 = SnailNumber::new(line1);
			let n2_1 = SnailNumber::new(line2);
			let m1 = SnailNumber::add_consume(n1_1, n2_1).magnitude();

			let n1_2 = SnailNumber::new(line1);
			let n2_2 = SnailNumber::new(line2);
			let m2 = SnailNumber::add_consume(n2_2, n1_2).magnitude();

			best_magnitude = std::cmp::max(best_magnitude, m1);
			best_magnitude = std::cmp::max(best_magnitude, m2);
		}
	}
	
	best_magnitude
}

#[derive(Debug,Clone,Copy,PartialEq)]
enum Direction {
	Left,
	Right, 
	NoDir
}

#[derive(Debug)]
struct SnailNumber {
	left : Option<Box<SnailNumber>>,
	right : Option<Box<SnailNumber>>,
	leaf_content : Option<u8>,
	child_dir : Direction,
}

impl SnailNumber {
	fn empty() -> SnailNumber {
		SnailNumber {
			left : None,
			right : None,
			leaf_content : None,
			child_dir : Direction::NoDir, 
		}
	}	

	fn leaf(val : u8) -> SnailNumber {
		SnailNumber {
			left : None,
			right : None,
			leaf_content : Some(val),
			child_dir : Direction::NoDir, 
		}
	}

	pub fn new(input : &str) -> SnailNumber {
		let mut stack = Vec::<SnailNumber>::new();
		for ch in input.chars(){
			match ch {
				'[' => {
					stack.push(SnailNumber::empty()) 
				},
				']' => { 
					if stack.len() > 1 { // Leave the last pop for returning
						let mut finished_node = stack.pop().unwrap();
						let mut current_node = stack.last_mut().unwrap();
						if !current_node.left.is_some() {
							finished_node.child_dir = Direction::Left;
							current_node.left = Some(Box::new(finished_node));
						} else {
							finished_node.child_dir = Direction::Right;
							current_node.right = Some(Box::new(finished_node));
						} 
					}
				},
				',' => {},
				x => {
					let mut new_node = SnailNumber::leaf(x.to_digit(10).unwrap() as u8);
					let mut current_node = stack.last_mut().unwrap();
					if !current_node.left.is_some() {
						new_node.child_dir = Direction::Left;
						current_node.left = Some(Box::new(new_node));
					} else {
						new_node.child_dir = Direction::Right;
						current_node.right = Some(Box::new(new_node));
					}	
				} 
			}
		}
		stack.pop().unwrap()
	}
	
	fn add_consume(mut first : SnailNumber, mut second: SnailNumber) -> SnailNumber {
		//println!("Adding {} + {}", first, second);
		let mut new = SnailNumber::empty();
		first.child_dir  = Direction::Left;
		new.left = Some(Box::new(first));
		second.child_dir  = Direction::Right;
		new.right = Some(Box::new(second));
		//println!("---------- Result before reduce {}", new);
		new.reduce();
		//println!("---------- Result after reduce {}", new);
		new
    }

	fn sum_consume(to_sum : &mut Vec<SnailNumber>) -> SnailNumber{
		//println!("consuming  ---- {}", to_sum[0]);
		//println!("consuming  ---- {}", to_sum[1]);
		let mut acum = to_sum.remove(0);
		while to_sum.len() > 0 {
			acum = SnailNumber::add_consume(acum, to_sum.remove(0));
		}		
		acum
	}

	
	
	pub fn is_leaf(&self) -> bool {
		self.leaf_content.is_some()
	}

	pub fn is_concrete_pair(&self) -> bool {
		!self.is_leaf() && self.left.as_ref().unwrap().is_leaf() && self.right.as_ref().unwrap().is_leaf()
	}

	pub fn magnitude(&self) -> u64 {
		if self.is_leaf() {
			return self.leaf_content.unwrap() as u64;
		} else {
			return 3 * self.left.as_ref().unwrap().magnitude() + 2 * self.right.as_ref().unwrap().magnitude(); 
		}
	}

	pub fn reduce(&mut self) {
		// Going unsafe here because it's a pain in the ass otherwise
		//println!("-- Reducing {}", self);
		let mut order : Vec<*mut SnailNumber> = Vec::new();
		loop {
			order.clear();
			//println!("---------------- root is {}", self);
			order.push(self);
			if self.sub_explode(0, &mut order) {
				continue;
			}
			order.clear();
			order.push(self);
			if self.sub_split(0, &mut order) {
				continue;
			}
			break;
		};
	} 

	fn sub_explode(&mut self, depth : usize, order : &mut Vec<*mut SnailNumber>) -> bool {
		//println!("---- Reducing {}", self);

		if depth >= 4 && self.is_concrete_pair() {
			//println!("------ Exploding {}", self);
			self.explode(order);
			return true;
		}

		if !self.leaf_content.is_some() {
			order.push(&mut *self.left.as_deref_mut().unwrap());
			let reduced_left = self.left.as_deref_mut().unwrap().sub_explode(depth + 1, order);
			order.pop(); 
			if reduced_left {
				return true;
			}

			order.push(&mut *self.right.as_deref_mut().unwrap());
			let reduced_right = self.right.as_deref_mut().unwrap().sub_explode(depth + 1, order);
			order.pop();
			if reduced_right {
				return true;
			}
		}

		false
	}

	fn sub_split(&mut self, depth : usize, order : &mut Vec<*mut SnailNumber>) -> bool {
		//println!("---- Reducing {}", self);
		// if order.len() > 0 { println!("---- root is {}", unsafe { &*order[0] } ); }

		if self.is_leaf() {
			let val = self.leaf_content.unwrap();
			if val >= 10 {
				//println!("------ Splitting {}", val);
				self.split(val);
				return true;
			}
		}

		if !self.leaf_content.is_some() {
			order.push(&mut *self.left.as_deref_mut().unwrap());
			let reduced_left = self.left.as_deref_mut().unwrap().sub_split(depth + 1, order);
			order.pop(); 
			if reduced_left {
				return true;
			}

			order.push(&mut *self.right.as_deref_mut().unwrap());
			let reduced_right = self.right.as_deref_mut().unwrap().sub_split(depth + 1, order);
			order.pop();
			if reduced_right {
				return true;
			}
		}

		false
	}

	fn split(&mut self, val : u8) {
		let left = val / 2;
		let right = val / 2 + val % 2; 
		let mut n_left = SnailNumber::leaf(left);
		let mut n_right = SnailNumber::leaf(right);
		n_left.child_dir = Direction::Left;
		n_right.child_dir = Direction::Right; 

		self.leaf_content = None;
		self.left = Some(Box::new(n_left));
		self.right = Some(Box::new(n_right));
	}

	fn explode(&mut self, order : &mut Vec<*mut SnailNumber>) {
		let mut leftn = self.left.as_ref().unwrap().leaf_content.unwrap();
		let mut rightn = self.right.as_ref().unwrap().leaf_content.unwrap();

		self.left = None;
		self.right = None;
		self.leaf_content = Some(0);
		order.pop();

		self.add_going_up(order, &mut leftn, &mut rightn);
	}
	
	fn add_going_up(&mut self, order : &mut Vec<*mut SnailNumber>, leftn: &mut u8, rightn: &mut u8) {
		//println!("going up from {} which is {:?} child, matching left {} right {}", self, self.child_dir, leftn, rightn);
		//if order.len() > 0 { println!("root is {}", unsafe { &*order[0] } ); }

		if order.len() == 0 || (*leftn == 0 && *rightn == 0) {
			return;
		}

		let parent = unsafe { &mut *order.pop().unwrap() };
		//println!("Reducing {:?}", order);
		//println!("Reducing {}", parent);

		if self.child_dir == Direction::Left && *rightn != 0{ // Visit the unvisited, which is to the right, then we go left down
			//println!("trying rightn");
			let next_node = parent.right.as_deref_mut().unwrap();	 	
			next_node.add_going_down(rightn, Direction::Left);
		} 
		else if self.child_dir == Direction::Right && *leftn != 0 {
			//println!("trying leftn");
			let next_node = parent.left.as_deref_mut().unwrap();
			next_node.add_going_down(leftn, Direction::Right);
		}

		parent.add_going_up(order, leftn, rightn);	
	}

	fn add_going_down(&mut self, val: &mut u8, visit : Direction) -> bool {
		//println!("going down at {} in direction {:?} with value {}", self, visit, *val);
		if self.is_leaf() {
			let res = self.leaf_content.unwrap() + *val;
			//println!("Adding to {} value {}", self, *val);
			*val = 0;
			self.leaf_content = Some(res);
			return true;
		} else {
			let left = self.left.as_deref_mut().unwrap();
			let right = self.right.as_deref_mut().unwrap();
			if visit == Direction::Left {				
				if left.add_going_down(val, visit) {
					return true;
				} 
			} else {
				if right.add_going_down(val, visit) {
					return true;
				} 
			}
		}
		return false;
	}

}

impl fmt::Display for SnailNumber {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
		if self.is_leaf() {
			return write!(f, "{}", self.leaf_content.unwrap());
		}
		else {
			return write!(f, "[{},{}]", self.left.as_ref().unwrap(), self.right.as_ref().unwrap());
		}
    }
}

#[cfg(test)]
mod tests {
	use super::*;

	#[test]
	fn test18_parse() {
		let n1 = SnailNumber::new("[1,2]");
		let n2 = SnailNumber::new("[[1,2],3]");
		let n3 = SnailNumber::new("[9,[8,7]]");
		let n4 = SnailNumber::new("[[1,9],[8,5]]");
		let n5 = SnailNumber::new("[[[[1,2],[3,4]],[[5,6],[7,8]]],9]");
		let n6 = SnailNumber::new("[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]");
		let n7 = SnailNumber::new("[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]");
		let n8 = SnailNumber::new("[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]");

		assert_eq!(format!("{}",n1),"[1,2]");
		assert_eq!(format!("{}",n2),"[[1,2],3]");
		assert_eq!(format!("{}",n3),"[9,[8,7]]");
		assert_eq!(format!("{}",n4),"[[1,9],[8,5]]");
		assert_eq!(format!("{}",n5),"[[[[1,2],[3,4]],[[5,6],[7,8]]],9]");
		assert_eq!(format!("{}",n6),"[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]");
		assert_eq!(format!("{}",n7),"[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]");
		assert_eq!(format!("{}",n8),"[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]");
	}

	#[test]
	fn test18_reduce() {
		let mut n1 = SnailNumber::new("[[[[[9,8],1],2],3],4]");
		let mut n2 = SnailNumber::new("[7,[6,[5,[4,[3,2]]]]]");
		let mut n3 = SnailNumber::new("[[6,[5,[4,[3,2]]]],1]");
		let mut n4 = SnailNumber::new("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]");
		let mut n5 = SnailNumber::new("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]");
		let mut n6 = SnailNumber::new("[[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]");

		n1.reduce();
		assert_eq!(format!("{}",n1),"[[[[0,9],2],3],4]");

		n2.reduce();
		assert_eq!(format!("{}",n2),"[7,[6,[5,[7,0]]]]");

		n3.reduce();
		assert_eq!(format!("{}",n3),"[[6,[5,[7,0]]],3]");

		n4.reduce();
		assert_eq!(format!("{}",n4),"[[3,[2,[8,0]]],[9,[5,[7,0]]]]");

		n5.reduce();
		assert_eq!(format!("{}",n5),"[[3,[2,[8,0]]],[9,[5,[7,0]]]]");

		n6.reduce();
		assert_eq!(format!("{}",n6),"[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]");

	}

	#[test]
	fn test18_add() {
		let n1 = SnailNumber::new("[1,2]");
		let n2 = SnailNumber::new("[[3,4],5]");
		let n3 = SnailNumber::add_consume(n1,n2);
		assert_eq!(format!("{}",n3),"[[1,2],[[3,4],5]]");

		let mut a1 : Vec<SnailNumber> = vec![SnailNumber::new("[1,1]"), SnailNumber::new("[2,2]"), SnailNumber::new("[3,3]"), SnailNumber::new("[4,4]")];
		let s1 : SnailNumber = SnailNumber::sum_consume(&mut a1);
		assert_eq!(format!("{}", s1),"[[[[1,1],[2,2]],[3,3]],[4,4]]");

		let mut a2 : Vec<SnailNumber> = vec![SnailNumber::new("[1,1]"), SnailNumber::new("[2,2]"), SnailNumber::new("[3,3]"), SnailNumber::new("[4,4]"), SnailNumber::new("[5,5]")];
		let s2 : SnailNumber = SnailNumber::sum_consume(&mut a2);
		assert_eq!(format!("{}", s2),"[[[[3,0],[5,3]],[4,4]],[5,5]]");

		let mut a3 : Vec<SnailNumber> = vec![SnailNumber::new("[1,1]"), SnailNumber::new("[2,2]"), SnailNumber::new("[3,3]"), SnailNumber::new("[4,4]"), SnailNumber::new("[5,5]"), SnailNumber::new("[6,6]")];
		let s3 : SnailNumber = SnailNumber::sum_consume(&mut a3);
		assert_eq!(format!("{}", s3),"[[[[5,0],[7,4]],[5,5]],[6,6]]");

		let mut a4 : Vec<SnailNumber> = vec![
			SnailNumber::new("[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]"), SnailNumber::new("[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]")
		];
		let s4 : SnailNumber = SnailNumber::sum_consume(&mut a4);
		assert_eq!(format!("{}", s4),"[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]");
	}

	#[test]
	fn test18_magnitude() {
		let n1 = SnailNumber::new("[9,1]");
		let n2 = SnailNumber::new("[[9,1],[1,9]]");
		let n3 = SnailNumber::new("[[1,2],[[3,4],5]]");
		let n4 = SnailNumber::new("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]");
		let n5 = SnailNumber::new("[[[[1,1],[2,2]],[3,3]],[4,4]]");
		let n6 = SnailNumber::new("[[[[3,0],[5,3]],[4,4]],[5,5]]");
		let n7 = SnailNumber::new("[[[[5,0],[7,4]],[5,5]],[6,6]]");
		let n8 = SnailNumber::new("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]");

		assert_eq!(29, n1.magnitude());
		assert_eq!(129, n2.magnitude());
		assert_eq!(143, n3.magnitude());
		assert_eq!(1384, n4.magnitude());
		assert_eq!(445, n5.magnitude());
		assert_eq!(791, n6.magnitude());
		assert_eq!(1137, n7.magnitude());
		assert_eq!(3488, n8.magnitude());
	}

	#[test]
	fn test18_1() {
		let input = &String::from("[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]\n[[[5,[2,8]],4],[5,[[9,9],0]]]\n[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]\n[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]\n[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]\n[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]\n[[[[5,4],[7,7]],8],[[8,3],8]]\n[[9,3],[[9,9],[6,[4,9]]]]\n[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]\n[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]\n");
		assert_eq!(4140, day18_1(&input));
	}

	#[test]
	fn test18_2() {
		let input = &String::from("[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]\n[[[5,[2,8]],4],[5,[[9,9],0]]]\n[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]\n[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]\n[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]\n[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]\n[[[[5,4],[7,7]],8],[[8,3],8]]\n[[9,3],[[9,9],[6,[4,9]]]]\n[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]\n[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]\n");
		assert_eq!(3993,day18_2(input));
	}
}