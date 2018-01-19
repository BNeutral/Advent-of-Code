use std::fmt;

#[allow(dead_code)]
pub fn advent19_1(input : &str) -> String  {
    follow_route(input).0
}

#[allow(dead_code)]
pub fn advent19_2(input : &str) -> u32  {
    follow_route(input).1
}

/// Struct that represents a route + packet that moves in it
struct Route {
    grid : Vec<Vec<char>>,
}

const POSSIBLE_MOVES : [(i32,i32); 4] = [ (0,1) , (0,-1) , (1,0) , (-1,0) ];

impl Route {
    fn from(input : &str) -> Route {
        let mut grid : Vec<Vec<char>> = Vec::new();
        for line in input.lines() {
            grid.push(line.chars().collect::<Vec<char>>());
        }
        Route {
            grid : grid,
        }
    }

    /// Moves the packet to the end of the maze and returns the visited letters
    fn move_to_end(&mut self) -> (String,u32) {
        let mut visited = String::new();
        let mut current_pos : (i32,i32) = (self.grid[0].iter().position(|&x| { x == '|' }).unwrap() as i32,0);
        let mut current_dir : (i32,i32) = (0,1);
        let mut steps = 0;
        loop {
            let previous_pos = current_pos;
            current_pos = add_tuple(current_pos, current_dir);
            steps += 1;
            let current_char = self.get_char(current_pos.0, current_pos.1);
            match current_char {
                '+' => { current_dir = self.find_next_dir(current_pos, previous_pos); },
                '|' => {},
                '-' => {},
                ' ' => break,
                _ => visited.push(current_char),
            }
        }
        (visited, steps)
    }

    /// Find the next direction to move, if none is found returns (0,0)
    fn find_next_dir(&self, current_pos : (i32,i32), previous_pos : (i32,i32) ) -> (i32,i32) {
        for &(x,y) in POSSIBLE_MOVES.iter() {
            let possibility : (i32,i32) = add_tuple(current_pos, (x,y));
            if possibility == previous_pos { continue; }
            let character = self.get_char(possibility.0,possibility.1);
            if !character.is_whitespace() {
                return (x,y)
            }
        }
        (0,0)
    }

    /// Returns the character at position X,Y of the grid
    fn get_char(&self, x : i32, y : i32) -> char {
        if y < 0 || x < 0 { return ' ' }
        let x = x as usize;
        let y = y as usize;
        if y >= self.grid.len() || x >= self.grid[y].len() { return ' ' }
        self.grid[y][x]
    }
}


#[allow(unused_must_use)]
impl fmt::Display for Route {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        for row in &self.grid {
            for c in row {
                write!(f, "{}", c);
            }
            write!(f, "\n");
        }
        write!(f, "\n")
    }
}

/// Walks the ASCII maze and returns the sequence of visited letters
/// Assumes the input is formated as the problem says
/// Location corresponds to a |‾ coordinate system x right, y down
fn follow_route(input : &str) -> (String,u32) {
    let mut route : Route = Route::from(input);
    route.move_to_end()
}

use std::ops::Add;

fn add_tuple<T : Add<Output=T>>(t1 : (T,T), t2 : (T,T)) -> (T,T) {
    (t1.0 + t2.0, t1.1 + t2.1)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test1_1() {
        let input = "     |          \n     |  +--+    \n     A  |  C    \n F---|----E|--+ \n     |  |  |  D \n     +B-+  +--+ ";
        assert_eq!("ABCDEF",advent19_1(input));
    }

    #[test]
    fn test2_1() {
        let input = "     |          \n     |  +--+    \n     A  |  C    \n F---|----E|--+ \n     |  |  |  D \n     +B-+  +--+ ";
        assert_eq!(38,advent19_2(input));
    }

}