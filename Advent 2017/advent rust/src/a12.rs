use std::collections::HashSet;

#[allow(dead_code)]
pub fn advent12_1(input : &str) -> usize {
    solve(input, false)
}

#[allow(dead_code)]
pub fn advent12_2(input : &str) -> usize {
    solve(input, true)
}

/// Finds the amount of nodes connected to the 0 node if second_part is false
/// Otherwise finds the amount of different disconnected groups
/// Assumes the input is properly formatted and ordered
/// Proper format is of the type "pid0 <-> pid1,pid2,...,pidn"
/// Where pid0 matches with the current line number
fn solve(input : &str, second_part : bool) -> usize {
    let lines = input.trim().replace(" ","");
    let lines : Vec<&str>  = lines.lines().collect();
    let line_count = lines.len();
    let mut visited_pids : HashSet<usize> = HashSet::new();
    let mut pids_to_check : Vec<usize> = vec![0];
    let mut line_counter : usize = 0;
    let mut number_of_groups : usize = 1;

    while visited_pids.len() < line_count {
        if pids_to_check.is_empty() {
            if !second_part { return visited_pids.len() }
            while visited_pids.contains(&line_counter) {
                line_counter += 1;
            }
            pids_to_check.push(line_counter);
            number_of_groups += 1;
            continue;
        }

        let current_pid = pids_to_check.pop().unwrap();
        if visited_pids.contains(&current_pid) { continue; }
        visited_pids.insert(current_pid);
        let line = lines[current_pid];
        let connections : Vec<&str> = line.split("<->").last().unwrap().split(",").collect();
        for pid in connections {
            let pid = pid.parse::<usize>().unwrap();
            pids_to_check.push(pid);
        }
    }
    number_of_groups
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test1_1() {
        let input = "0 <-> 2\n1 <-> 1\n2 <-> 0, 3, 4\n\
        3 <-> 2, 4\n4 <-> 2, 3, 6\n5 <-> 6\n6 <-> 4, 5";
        assert_eq!(6, advent12_1(input));
    }

}