use std::ops::Add;
use std::ops::Sub;
use std::ops::Neg;
use std::fmt;
use std::collections::HashMap;
use std::collections::HashSet;

#[allow(dead_code)]
pub fn day19(input : &String) -> () {
	let (part1, part2) = solve(input);
	println!("Part1: {}", part1);
	println!("Part2: {}", part2);
}

pub fn solve(input : &String) -> (usize,usize) {
	let mut scanners = parse(input);

	let mut matched : HashSet<usize> = HashSet::new();
	let mut scanner_positions : Vec<IntVector3> = Vec::new();
	matched.insert(0);

	while matched.len() < scanners.len() {
		for x in 0..scanners.len() {
			if !matched.contains(&x) {
				continue;
			}	
			for y in 1..scanners.len() {	
				if matched.contains(&y) {
					continue;
				}	
				let (overlaps, pos, rot) = scanners[x].overlaps(&scanners[y]);
				if overlaps {
					matched.insert(y);
					scanners[y].align_rot_pos(rot, pos);
					scanner_positions.push(pos); 
				}
			}
		}
	}
	
	let mut world_pos : HashSet<IntVector3> = HashSet::new(); 
	for scan in scanners {
		for beac in scan.beacons {
			world_pos.insert(beac);
		}
	}

	let mut best_distance = 0;
	for pos1 in scanner_positions.iter() {
		for pos2 in scanner_positions.iter() {
			let dist = pos1.mahattan(pos2);
			best_distance = std::cmp::max(best_distance, dist);
		}
	}

	(world_pos.len(),best_distance as usize)
}

#[allow(dead_code)]
pub fn day19_1(input : &String) -> usize {
	solve(input).0
}

#[allow(dead_code)]
pub fn day19_2(input : &String) -> usize {
	solve(input).1
}

pub fn parse(input : &String) -> Vec<Scanner> {
	let mut result : Vec<Scanner> = Vec::new();
	for line in input.lines() {
		if line.is_empty() {
			continue;
		}
		if line.contains("---") {
			result.push(Scanner::new());
		}
		else {
			result.last_mut().unwrap().beacons.push(IntVector3::from(line));
		}
	}
	result
}

#[derive(Debug)]
pub struct Scanner {
	beacons : Vec<IntVector3>
}

impl Scanner {
	pub fn new() -> Scanner {
		Scanner {
			beacons : Vec::new()
		}
	}

	pub fn expand_beacons_rotations(&self) ->  Vec<Vec<IntVector3>> {
		let mut rotations : Vec<Vec<IntVector3>> = Vec::new();
		for x in 0..24 {
			rotations.push(Vec::new());
			for point in self.beacons.iter() {
				rotations[x].push(point.get_rotation_fast(x));
			}
		} 
		rotations
	}

	// Returns if a match is found, the position (relative to self) and the rotation id
	pub fn overlaps(&self, other : &Scanner) -> (bool, IntVector3,usize) {
		let mut rotation_count = 0;
		for rotated_points in other.expand_beacons_rotations() {
			let mut guesses : HashMap<IntVector3, usize> = HashMap::new();

			for point1 in self.beacons.iter() {
				for point2 in rotated_points.iter() {
					let guess = (*point1) - (*point2);
					*guesses.entry(guess).or_insert(0) += 1
				}
			}
		
			for guess in guesses {
				if guess.1 >= 12 {
					return (true, guess.0, rotation_count);
				}
			}
			rotation_count += 1;
		}

		(false, IntVector3::zero(),0)
	}

	pub fn align_rot_pos(&mut self, rotation_id : usize, pos : IntVector3) {
		let mut rotations : Vec<IntVector3> = Vec::new();
		for beac in self.beacons.iter() {
			rotations.push(beac.get_rotation_fast(rotation_id) + pos);
		} 
		self.beacons = rotations;
	} 
	
}

// Was wasting time searching for a library with these things, so just rolled my own
#[derive(Debug, Clone, Copy, Eq, PartialEq, Hash, Ord, PartialOrd)]
pub struct IntVector3 {
	x : i32,
	y : i32,
	z : i32 
}

impl Add for IntVector3 {
    type Output = Self;
    fn add(self, other: Self) -> Self {
        Self {
            x: self.x + other.x,
            y: self.y + other.y,
			z: self.z + other.z
        }
    }
}

impl Sub for IntVector3 {
    type Output = Self;
    fn sub(self, other: Self) -> Self {
        Self {
            x: self.x - other.x,
            y: self.y - other.y,
			z: self.z - other.z
        }
    }
}

impl Neg for IntVector3 {
    type Output = Self;
    fn neg(self) -> Self {
        Self {
            x: - self.x,
            y: - self.y,
			z: - self.z
        }
    }
}

impl fmt::Display for IntVector3 {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
		return write!(f, "[{},{},{}]", self.x, self.y, self.z);
    }
}

#[allow(dead_code)]
impl IntVector3 {
	pub fn new(x : i32, y : i32, z : i32) -> IntVector3 {
		IntVector3 {
			x : x,
			y : y,
			z : z 
		}
	}

	pub fn zero() -> IntVector3 {
		IntVector3 {
			x : 0,
			y : 0,
			z : 0 
		}
	}

	pub fn from(input : &str) -> IntVector3  {
		let split : Vec<&str> = input.split(",").collect();
		IntVector3 {
			x : split[0].trim().parse().unwrap(),
			y : split[1].trim().parse().unwrap(),
			z : split[2].trim().parse().unwrap() 
		}
	}

	fn _rotate_z_90(&self) -> IntVector3 {
		IntVector3 {
			x : self.y,
			y : -self.x,
			z : self.z 
		}
	}

	fn _rotate_y_90(&self) -> IntVector3 {
		IntVector3 {
			x : self.z,
			y : self.y,
			z : -self.x 
		}
	} 

	fn _rotate_x_90(&self) -> IntVector3 {
		IntVector3 {
			x : self.x,
			y : -self.z,
			z : self.y 
		}
	} 

	pub fn get_all_rotations(&self) -> Vec<IntVector3> {
		let mut all = Vec::new();

		for x in 0..24 {
			all.push(self.get_rotation_fast(x));
		}

		all
	}

	pub fn get_rotation_fast(&self, id : usize) -> IntVector3 {
		let mut result = IntVector3::zero();
		match id {
			0 => { result.x = self.x; result.y = self.y; result.z = self.z },
			1 => { result.x = self.x; result.y = -self.z; result.z = self.y },
			2 => { result.x = self.z; result.y = self.y; result.z = -self.x },
			3 => { result.x = self.y; result.y = -self.x; result.z = self.z },
			4 => { result.x = self.x; result.y = -self.y; result.z = -self.z },
			5 => { result.x = self.y; result.y = -self.z; result.z = -self.x },
			6 => { result.x = -self.z; result.y = -self.x; result.z = self.y },
			7 => { result.x = self.z; result.y = self.x; result.z = self.y },
			8 => { result.x = -self.x; result.y = self.y; result.z = -self.z },
			9 => { result.x = self.z; result.y = -self.x; result.z = -self.y },
			10 => { result.x = -self.x; result.y = -self.y; result.z = self.z },
			11 => { result.x = self.x; result.y = self.z; result.z = -self.y },
			12 => { result.x = -self.z; result.y = -self.y; result.z = -self.x },
			13 => { result.x = -self.y; result.y = -self.x; result.z = -self.z },
			14 => { result.x = self.y; result.y = self.x; result.z = -self.z },
			15 => { result.x = -self.x; result.y = -self.z; result.z = -self.y },
			16 => { result.x = -self.x; result.y = self.z; result.z = self.y },
			17 => { result.x = self.z; result.y = -self.y; result.z = self.x },
			18 => { result.x = -self.z; result.y = self.y; result.z = self.x },
			19 => { result.x = -self.y; result.y = self.x; result.z = self.z },
			20 => { result.x = -self.y; result.y = self.z; result.z = -self.x },
			21 => { result.x = -self.z; result.y = self.x; result.z = -self.y },
			22 => { result.x = self.y; result.y = self.z; result.z = self.x },
			23 => { result.x = -self.y; result.y = -self.z; result.z = self.x },
			_ => panic!("Bad rotation")
		}
		result
	}

	
	pub fn _get_rotation_slow(&self, id : usize) -> IntVector3 {
		let result : IntVector3;
		match id {
			0 => { result = self.clone(); },
			1 => { result = self._rotate_x_90() },
			2 => { result = self._rotate_y_90() },
			3 => { result = self._rotate_z_90() },
			4 => { result = self._rotate_x_90()._rotate_x_90() },
			5 => { result = self._rotate_x_90()._rotate_y_90() },
			6 => { result = self._rotate_x_90()._rotate_z_90() },
			7 => { result = self._rotate_y_90()._rotate_x_90() },
			8 => { result = self._rotate_y_90()._rotate_y_90() },
			9 => { result = self._rotate_z_90()._rotate_y_90() },
			10 => { result = self._rotate_z_90()._rotate_z_90() },
			11 => { result = self._rotate_x_90()._rotate_x_90()._rotate_x_90() },
			12 => { result = self._rotate_x_90()._rotate_x_90()._rotate_y_90() },
			13 => { result = self._rotate_x_90()._rotate_x_90()._rotate_z_90() },
			14 => { result = self._rotate_x_90()._rotate_y_90()._rotate_x_90() },
			15 => { result = self._rotate_x_90()._rotate_y_90()._rotate_y_90() },
			16 => { result = self._rotate_x_90()._rotate_z_90()._rotate_z_90() },
			17 => { result = self._rotate_y_90()._rotate_x_90()._rotate_x_90() },
			18 => { result = self._rotate_y_90()._rotate_y_90()._rotate_y_90() },
			19 => { result = self._rotate_z_90()._rotate_z_90()._rotate_z_90() },
			20 => { result = self._rotate_x_90()._rotate_x_90()._rotate_x_90()._rotate_y_90() },
			21 => { result = self._rotate_x_90()._rotate_x_90()._rotate_y_90()._rotate_x_90() },
			22 => { result = self._rotate_x_90()._rotate_y_90()._rotate_x_90()._rotate_x_90() },
			23 => { result = self._rotate_x_90()._rotate_y_90()._rotate_y_90()._rotate_y_90() },
			_ => panic!("Bad rotation")
		}
		result
	}

	pub fn mahattan(&self, other : &IntVector3) -> i32 {
		let tmp = *self - *other;
		i32::abs(tmp.x)+i32::abs(tmp.y)+i32::abs(tmp.z)
	}
}

#[cfg(test)]
mod tests {
	use super::*;
	use std::iter::FromIterator;

	#[test]
	fn test19_parse() {
		let point = IntVector3::from("1, -2, 33");
		assert_eq!(IntVector3::new(1, -2, 33), point);

		let res = parse(&String::from("--- scanner 0 ---\n404,-588,-901\n528,-643,409\n-838,591,734\n390,-675,-793\n-537,-823,-458\n-485,-357,347\n-345,-311,381\n-661,-816,-575\n-876,649,763\n-618,-824,-621\n553,345,-567\n474,580,667\n-447,-329,318\n-584,868,-557\n544,-627,-890\n564,392,-477\n455,729,728\n-892,524,684\n-689,845,-530\n423,-701,434\n7,-33,-71\n630,319,-379\n443,580,662\n-789,900,-551\n459,-707,401\n\n--- scanner 1 ---\n686,422,578\n605,423,415\n515,917,-361\n-336,658,858\n95,138,22\n-476,619,847\n-340,-569,-846\n567,-361,727\n-460,603,-452\n669,-402,600\n729,430,532\n-500,-761,534\n-322,571,750\n-466,-666,-811\n-429,-592,574\n-355,545,-477\n703,-491,-529\n-328,-685,520\n413,935,-424\n-391,539,-444\n586,-435,557\n-364,-763,-893\n807,-499,-711\n755,-354,-619\n553,889,-390\n\n--- scanner 2 ---\n649,640,665\n682,-795,504\n-784,533,-524\n-644,584,-595\n-588,-843,648\n-30,6,44\n-674,560,763\n500,723,-460\n609,671,-379\n-555,-800,653\n-675,-892,-343\n697,-426,-610\n578,704,681\n493,664,-388\n-671,-858,530\n-667,343,800\n571,-461,-707\n-138,-166,112\n-889,563,-600\n646,-828,498\n640,759,510\n-630,509,768\n-681,-892,-333\n673,-379,-804\n-742,-814,-386\n577,-820,562\n\n--- scanner 3 ---\n-589,542,597\n605,-692,669\n-500,565,-823\n-660,373,557\n-458,-679,-417\n-488,449,543\n-626,468,-788\n338,-750,-386\n528,-832,-391\n562,-778,733\n-938,-730,414\n543,643,-506\n-524,371,-870\n407,773,750\n-104,29,83\n378,-903,-323\n-778,-728,485\n426,699,580\n-438,-605,-362\n-469,-447,-387\n509,732,623\n647,635,-688\n-868,-804,481\n614,-800,639\n595,780,-596\n\n--- scanner 4 ---\n727,592,562\n-293,-554,779\n441,611,-461\n-714,465,-776\n-743,427,-804\n-660,-479,-426\n832,-632,460\n927,-485,-438\n408,393,-506\n466,436,-512\n110,16,151\n-258,-428,682\n-393,719,612\n-211,-452,876\n808,-476,-593\n-575,615,604\n-485,667,467\n-680,325,-822\n-627,-443,-432\n872,-547,-609\n833,512,582\n807,604,487\n839,-516,451\n891,-625,532\n-652,-548,-490\n30,-46,-14\n"));
		assert_eq!(5, res.len());
		assert_eq!(25, res[0].beacons.len());
		assert_eq!(IntVector3::from("404,-588,-901"), res[0].beacons[0]);
		assert_eq!(IntVector3::from("459,-707,401"), res[0].beacons[24]);
	}

	#[test]
	fn test19_rotations() {
		let point = IntVector3::new(1, 2, 3);
		let rotations = point.get_all_rotations();
		// Code to output faster code. Just keeping it here in case something is wrong.
		/*let mut count = 0;
		let mut map : HashMap<i32, &str>= HashMap::new();
		map.insert(1, "self.x");
		map.insert(-1, "-self.x");
		map.insert(2, "self.y");
		map.insert(-2, "-self.y");
		map.insert(3, "self.z");
		map.insert(-3, "-self.z");
		for rot in rotations.iter() {
			println!("{} => {{ result.x = {}; result.y = {}; result.z = {} }},",count,map[&rot.x],map[&rot.y],map[&rot.z]);			
			count += 1;
		}*/
		let set : HashSet<IntVector3> = HashSet::from_iter(rotations);
		assert_eq!(24, set.len());

		let point = IntVector3::new(5, 6, -4);
		let rotations = point.get_all_rotations();
		let set : HashSet<IntVector3> = HashSet::from_iter(rotations);
		assert!(set.contains(&IntVector3::new(5, 6, -4)));
		assert!(set.contains(&IntVector3::new(-5, 4, -6)));
		assert!(set.contains(&IntVector3::new(4, 6, 5)));
		assert!(set.contains(&IntVector3::new(-4, -6, 5)));
		assert!(set.contains(&IntVector3::new(-6, -4, -5)));
	}

	#[test]
	fn test19_overlap() {
		let input = String::from("--- scanner 0 ---\n404,-588,-901\n528,-643,409\n-838,591,734\n390,-675,-793\n-537,-823,-458\n-485,-357,347\n-345,-311,381\n-661,-816,-575\n-876,649,763\n-618,-824,-621\n553,345,-567\n474,580,667\n-447,-329,318\n-584,868,-557\n544,-627,-890\n564,392,-477\n455,729,728\n-892,524,684\n-689,845,-530\n423,-701,434\n7,-33,-71\n630,319,-379\n443,580,662\n-789,900,-551\n459,-707,401\n\n--- scanner 1 ---\n686,422,578\n605,423,415\n515,917,-361\n-336,658,858\n95,138,22\n-476,619,847\n-340,-569,-846\n567,-361,727\n-460,603,-452\n669,-402,600\n729,430,532\n-500,-761,534\n-322,571,750\n-466,-666,-811\n-429,-592,574\n-355,545,-477\n703,-491,-529\n-328,-685,520\n413,935,-424\n-391,539,-444\n586,-435,557\n-364,-763,-893\n807,-499,-711\n755,-354,-619\n553,889,-390\n\n--- scanner 2 ---\n649,640,665\n682,-795,504\n-784,533,-524\n-644,584,-595\n-588,-843,648\n-30,6,44\n-674,560,763\n500,723,-460\n609,671,-379\n-555,-800,653\n-675,-892,-343\n697,-426,-610\n578,704,681\n493,664,-388\n-671,-858,530\n-667,343,800\n571,-461,-707\n-138,-166,112\n-889,563,-600\n646,-828,498\n640,759,510\n-630,509,768\n-681,-892,-333\n673,-379,-804\n-742,-814,-386\n577,-820,562\n\n--- scanner 3 ---\n-589,542,597\n605,-692,669\n-500,565,-823\n-660,373,557\n-458,-679,-417\n-488,449,543\n-626,468,-788\n338,-750,-386\n528,-832,-391\n562,-778,733\n-938,-730,414\n543,643,-506\n-524,371,-870\n407,773,750\n-104,29,83\n378,-903,-323\n-778,-728,485\n426,699,580\n-438,-605,-362\n-469,-447,-387\n509,732,623\n647,635,-688\n-868,-804,481\n614,-800,639\n595,780,-596\n\n--- scanner 4 ---\n727,592,562\n-293,-554,779\n441,611,-461\n-714,465,-776\n-743,427,-804\n-660,-479,-426\n832,-632,460\n927,-485,-438\n408,393,-506\n466,436,-512\n110,16,151\n-258,-428,682\n-393,719,612\n-211,-452,876\n808,-476,-593\n-575,615,604\n-485,667,467\n-680,325,-822\n-627,-443,-432\n872,-547,-609\n833,512,582\n807,604,487\n839,-516,451\n891,-625,532\n-652,-548,-490\n30,-46,-14\n");
		let mut scanners = parse(&input);
		
		let (overlaps01, pos1, rot1) = scanners[0].overlaps(&scanners[1]);
		assert_eq!(true, overlaps01);
		assert_eq!(IntVector3::from("68,-1246,-43"), pos1);
		scanners[1].align_rot_pos(rot1, pos1);

		let (overlaps14, pos4, rot4) = scanners[1].overlaps(&scanners[4]);
		assert_eq!(true, overlaps14);
		assert_eq!(IntVector3::from("-20,-1133,1061"), pos4);
		scanners[4].align_rot_pos(rot4, pos4);

		let (overlaps42, pos2, rot2) = scanners[4].overlaps(&scanners[2]);
		assert_eq!(true, overlaps42);
		assert_eq!(IntVector3::from("1105,-1205,1229"), pos2);
		scanners[2].align_rot_pos(rot2, pos2);

		let (overlaps13, pos3, rot3) = scanners[1].overlaps(&scanners[3]);
		assert_eq!(true, overlaps13);
		assert_eq!(IntVector3::from("-92,-2380,-20"), pos3);
		scanners[3].align_rot_pos(rot3, pos3);

		let mut world_pos : HashSet<IntVector3> = HashSet::new(); 
		for scan in scanners {
			for beac in scan.beacons {
				world_pos.insert(beac);
			}
		}

		assert_eq!(79, world_pos.len());
	}

	#[test]
	fn test19_1() {
		let input = String::from("--- scanner 0 ---\n404,-588,-901\n528,-643,409\n-838,591,734\n390,-675,-793\n-537,-823,-458\n-485,-357,347\n-345,-311,381\n-661,-816,-575\n-876,649,763\n-618,-824,-621\n553,345,-567\n474,580,667\n-447,-329,318\n-584,868,-557\n544,-627,-890\n564,392,-477\n455,729,728\n-892,524,684\n-689,845,-530\n423,-701,434\n7,-33,-71\n630,319,-379\n443,580,662\n-789,900,-551\n459,-707,401\n\n--- scanner 1 ---\n686,422,578\n605,423,415\n515,917,-361\n-336,658,858\n95,138,22\n-476,619,847\n-340,-569,-846\n567,-361,727\n-460,603,-452\n669,-402,600\n729,430,532\n-500,-761,534\n-322,571,750\n-466,-666,-811\n-429,-592,574\n-355,545,-477\n703,-491,-529\n-328,-685,520\n413,935,-424\n-391,539,-444\n586,-435,557\n-364,-763,-893\n807,-499,-711\n755,-354,-619\n553,889,-390\n\n--- scanner 2 ---\n649,640,665\n682,-795,504\n-784,533,-524\n-644,584,-595\n-588,-843,648\n-30,6,44\n-674,560,763\n500,723,-460\n609,671,-379\n-555,-800,653\n-675,-892,-343\n697,-426,-610\n578,704,681\n493,664,-388\n-671,-858,530\n-667,343,800\n571,-461,-707\n-138,-166,112\n-889,563,-600\n646,-828,498\n640,759,510\n-630,509,768\n-681,-892,-333\n673,-379,-804\n-742,-814,-386\n577,-820,562\n\n--- scanner 3 ---\n-589,542,597\n605,-692,669\n-500,565,-823\n-660,373,557\n-458,-679,-417\n-488,449,543\n-626,468,-788\n338,-750,-386\n528,-832,-391\n562,-778,733\n-938,-730,414\n543,643,-506\n-524,371,-870\n407,773,750\n-104,29,83\n378,-903,-323\n-778,-728,485\n426,699,580\n-438,-605,-362\n-469,-447,-387\n509,732,623\n647,635,-688\n-868,-804,481\n614,-800,639\n595,780,-596\n\n--- scanner 4 ---\n727,592,562\n-293,-554,779\n441,611,-461\n-714,465,-776\n-743,427,-804\n-660,-479,-426\n832,-632,460\n927,-485,-438\n408,393,-506\n466,436,-512\n110,16,151\n-258,-428,682\n-393,719,612\n-211,-452,876\n808,-476,-593\n-575,615,604\n-485,667,467\n-680,325,-822\n-627,-443,-432\n872,-547,-609\n833,512,582\n807,604,487\n839,-516,451\n891,-625,532\n-652,-548,-490\n30,-46,-14\n");
		assert_eq!(79, day19_1(&input));
	}

	#[test]
	fn test19_2() {
		let input = String::from("--- scanner 0 ---\n404,-588,-901\n528,-643,409\n-838,591,734\n390,-675,-793\n-537,-823,-458\n-485,-357,347\n-345,-311,381\n-661,-816,-575\n-876,649,763\n-618,-824,-621\n553,345,-567\n474,580,667\n-447,-329,318\n-584,868,-557\n544,-627,-890\n564,392,-477\n455,729,728\n-892,524,684\n-689,845,-530\n423,-701,434\n7,-33,-71\n630,319,-379\n443,580,662\n-789,900,-551\n459,-707,401\n\n--- scanner 1 ---\n686,422,578\n605,423,415\n515,917,-361\n-336,658,858\n95,138,22\n-476,619,847\n-340,-569,-846\n567,-361,727\n-460,603,-452\n669,-402,600\n729,430,532\n-500,-761,534\n-322,571,750\n-466,-666,-811\n-429,-592,574\n-355,545,-477\n703,-491,-529\n-328,-685,520\n413,935,-424\n-391,539,-444\n586,-435,557\n-364,-763,-893\n807,-499,-711\n755,-354,-619\n553,889,-390\n\n--- scanner 2 ---\n649,640,665\n682,-795,504\n-784,533,-524\n-644,584,-595\n-588,-843,648\n-30,6,44\n-674,560,763\n500,723,-460\n609,671,-379\n-555,-800,653\n-675,-892,-343\n697,-426,-610\n578,704,681\n493,664,-388\n-671,-858,530\n-667,343,800\n571,-461,-707\n-138,-166,112\n-889,563,-600\n646,-828,498\n640,759,510\n-630,509,768\n-681,-892,-333\n673,-379,-804\n-742,-814,-386\n577,-820,562\n\n--- scanner 3 ---\n-589,542,597\n605,-692,669\n-500,565,-823\n-660,373,557\n-458,-679,-417\n-488,449,543\n-626,468,-788\n338,-750,-386\n528,-832,-391\n562,-778,733\n-938,-730,414\n543,643,-506\n-524,371,-870\n407,773,750\n-104,29,83\n378,-903,-323\n-778,-728,485\n426,699,580\n-438,-605,-362\n-469,-447,-387\n509,732,623\n647,635,-688\n-868,-804,481\n614,-800,639\n595,780,-596\n\n--- scanner 4 ---\n727,592,562\n-293,-554,779\n441,611,-461\n-714,465,-776\n-743,427,-804\n-660,-479,-426\n832,-632,460\n927,-485,-438\n408,393,-506\n466,436,-512\n110,16,151\n-258,-428,682\n-393,719,612\n-211,-452,876\n808,-476,-593\n-575,615,604\n-485,667,467\n-680,325,-822\n-627,-443,-432\n872,-547,-609\n833,512,582\n807,604,487\n839,-516,451\n891,-625,532\n-652,-548,-490\n30,-46,-14\n");
		assert_eq!(3621, day19_2(&input));
	}
}