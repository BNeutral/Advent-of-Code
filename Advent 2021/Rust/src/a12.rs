use std::collections::HashMap;
use std::collections::HashSet;
use aoc::*;

#[allow(dead_code)]
pub fn day12(input : &String) -> () {
	println!("Part1: {}", day12_1(input));
	println!("Part2: {}", day12_2(input));
}

pub fn day12_1(input : &String) -> usize {
	let mut graph = StringyGraph::new();
	
	for line in input.lines() {
		let split = line.split('-').collect::<Vec<&str>>();
		graph.add_connection(&String::from(split[0]), &String::from(split[1]));
	}
	
	graph.find_all_paths(false)
}

pub fn day12_2(input : &String) -> usize {
	let mut graph = StringyGraph::new();
	
	for line in input.lines() {
		let split = line.split('-').collect::<Vec<&str>>();
		graph.add_connection(&String::from(split[0]), &String::from(split[1]));
	}
	
	graph.find_all_paths(true)
}

// Crappy implementation of a graph, if we were chasing performance we'd be using numeric indexes or something instead 
#[derive(Debug)]
pub struct StringyNode {
	name : String,
	is_small : bool,
	connections : Vec<String>
}

#[derive(Debug)]
pub struct StringyGraph {
	root : String,
	end : String,
	nodes : HashMap<String,StringyNode>
}

impl StringyGraph {
	pub fn new() -> StringyGraph {
		StringyGraph {
			root : String::from("start"),
			end : String::from("end"),
			nodes : HashMap::new()
		}
	}

	pub fn add_connection(&mut self, origin : &String, destination : &String) {
		self.create_node_if_needed(origin);
		self.create_node_if_needed(destination);
		if destination != &self.root {
			let node = self.nodes.get_mut(origin).unwrap();
			node.connections.push(destination.clone());
		}
		if destination != &self.end && origin != &self.root { // add origin to destination
			let node = self.nodes.get_mut(destination).unwrap();
			node.connections.push(origin.clone());
		}
	}

	pub fn find_all_paths(&self, visit_twice : bool) -> usize {
		let mut path_counter : usize = 0;
		let mut visited : HashSet<String> = HashSet::new();
		let mut visited_twice : String = String::new();
		self.traverse(&self.root, &mut path_counter, &mut visited, &mut visited_twice, visit_twice);
		path_counter
	}

	fn traverse(&self, node_key : &String, path_counter : &mut usize, visited : &mut HashSet<String>, 
		visited_twice : &mut String, visit_twice : bool) {
		if *node_key == self.end {
			*path_counter += 1;
			return;
		}

		let node = self.nodes.get(node_key).unwrap();
		if node.is_small {
			let already_visited = visited.contains(node_key);
			if already_visited {
				visited_twice.clone_from(node_key);
			}
			visited.insert(node_key.clone());
		}

		for next in &node.connections {
			let already_visited = visited.contains(next);
			if !already_visited || (visit_twice && visited_twice.is_empty()) {
				self.traverse(next, path_counter, visited, visited_twice, visit_twice);
			}
		}

		if visited_twice == node_key {
			visited_twice.clear();			
		} else {
			visited.remove(node_key);
		}
	}

	fn create_node_if_needed(&mut self, name : &String) {
		if !self.nodes.contains_key(name) {
			let node =  StringyNode{
				name: name.clone(),
				is_small: is_lowercase(name),
				connections: Vec::new()
			};
			self.nodes.insert(name.clone(), node);
		}
	}
}



#[cfg(test)]
mod tests {
	use super::*;

	#[test]
	fn test12_1() {
		let input = &String::from("start-A\nstart-b\nA-c\nA-b\nb-d\nA-end\nb-end\n");
		assert_eq!(10,day12_1(input));
	}

	#[test]
	fn test12_1_1() {
		let input = &String::from("dc-end\nHN-start\nstart-kj\ndc-start\ndc-HN\nLN-dc\nHN-end\nkj-sa\nkj-HN\nkj-dc\n");
		assert_eq!(19,day12_1(input));
	}

	#[test]
	fn test12_2() {
		let input = &String::from("start-A\nstart-b\nA-c\nA-b\nb-d\nA-end\nb-end\n");
		assert_eq!(36,day12_2(input));
	}

	#[test]
	fn test12_2_1() {
		let input = &String::from("dc-end\nHN-start\nstart-kj\ndc-start\ndc-HN\nLN-dc\nHN-end\nkj-sa\nkj-HN\nkj-dc\n");
		assert_eq!(103,day12_2(input));
	}

}