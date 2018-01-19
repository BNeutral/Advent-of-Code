use std::collections::HashMap;

struct Node {
    name: String,
    weight: u32,
    children: Vec<Node>,
}

impl Node {
    fn new(name: String, weight: u32) -> Node {
        Node {
            name,
            weight,
            children: Vec::new(),
        }
    }

    fn add_child(&mut self, node: Node) {
        self.children.push(node);
    }

    fn find_mismatched_weight(&self) -> Result<u32, u32> {
        if self.children.is_empty() {
            Ok(self.weight)
        } else {
            let mut result = self.weight;
            let mut child_counter: HashMap<u32, u32> = HashMap::new();
            let mut child_own_weight: HashMap<u32, u32> = HashMap::new();
            for child in &self.children {
                let weight = child.find_mismatched_weight()?;
                result += weight;
                *child_counter.entry(weight).or_insert(0) += 1;
                child_own_weight.insert(weight, child.weight);
            }
            if child_counter.len() > 1 {
                let mut culprit = 0;
                let mut other = 0;
                for (x, y) in &child_counter {
                    if *y == 1 { culprit = *x } else { other = *x }
                }
                let difference = {
                    if other > culprit {
                        other - culprit
                    } else {
                        culprit - other
                    }
                };
                let weight_to_change = child_own_weight.get(&culprit).unwrap();
                Err(weight_to_change - difference)
            } else {
                Ok(result)
            }

        }
    }
}

#[allow(dead_code)]
pub fn advent7_1(input: &str) -> String {
    let node = build_tree(input);
    node.name.clone()
}

#[allow(dead_code)]
pub fn advent7_2(input: &str) -> u32 {
    let node = build_tree(input);
    match node.find_mismatched_weight() {
        Ok(_) => panic!("Input was fine"),
        Err(x) => x,
    }
}

fn build_tree(s: &str) -> Node {
    let mut nodes: HashMap<String, Node> = HashMap::new();
    let mut connections: HashMap<String, Vec<String>> = HashMap::new();
    let mut root_name = "";
    for line in s.lines() {
        let mut name = "";
        let mut weight = 0;
        let mut split = line.split("->");
        match split.next() { // The part before the ->
            Some(s) => {
                let mut split_first = s.split_whitespace();
                match split_first.next() { // Name
                    Some(s) => {
                        name = s;
                    }
                    _ => {}
                }
                match split_first.next() { // Weight
                    Some(s) => {
                        let s = s.trim_matches(|c| c == '(' || c == ')');
                        weight = s.parse::<u32>().unwrap();
                    }
                    _ => {}
                }
            }
            _ => {}
        }

        match split.next() { // If it has children
            Some(s) => {
                if root_name == "" {
                    // If no root, add this
                    root_name = name;
                }
                let s = s.replace(" ", "");
                for child in s.split(",") {
                    if !connections.contains_key(name) {
                        connections.insert(String::from(name), Vec::new());
                    }
                    connections.get_mut(name).unwrap().push(String::from(child));
                    if child == root_name {
                        // If the root was mentioned as a child, the current node is the new root
                        root_name = name;
                    }
                }
            }
            _ => {}
        }

        nodes.insert(String::from(name), Node::new(String::from(name), weight));
    }
    let mut node: Node = nodes.remove(root_name).unwrap();
    connect_nodes(&mut node, &mut nodes, &mut connections);
    node
}

fn connect_nodes(mut node: &mut Node, mut nodes: &mut HashMap<String, Node>,
                 mut connections: &mut HashMap<String, Vec<String>>,) {
    match connections.remove(&node.name) { 
        Some(child_names) => {
            for child_name in child_names {
                let mut child = nodes.remove(&child_name).unwrap();
                connect_nodes(&mut child, &mut nodes, &mut connections);
                node.add_child(child);
            }
        }
        _ => {}
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test1() {
        let str = "pbga (66)\nxhth (57)\nebii (61)\nhavc (66)\nktlj (57)\nfwft (72) -> ktlj,\
         cntj, xhth\nqoyq (66)\npadx (45) -> pbga, havc, qoyq\ntknk (41) -> ugml, padx, fwft\njptl\
          (61)\nugml (68) -> gyxo, ebii, jptl\ngyxo (61)\ncntj (57)";
        assert_eq!("tknk", advent7_1(str));
    }

    #[test]
    fn test2() {
        let str = "pbga (66)\nxhth (57)\nebii (61)\nhavc (66)\nktlj (57)\nfwft (72) -> ktlj,\
         cntj, xhth\nqoyq (66)\npadx (45) -> pbga, havc, qoyq\ntknk (41) -> ugml, padx, fwft\njptl\
          (61)\nugml (68) -> gyxo, ebii, jptl\ngyxo (61)\ncntj (57)";
        assert_eq!(60, advent7_2(str));
    }

}
