use std::cmp;

#[allow(dead_code)]
pub fn advent11_1(input : &str) -> i32 {
    solve(input, false)
}

#[allow(dead_code)]
pub fn advent11_2(input : &str) -> i32 {
    solve(input, true)
}

/// Walks according to an input, then finds the shortest path to the final hex
fn solve(input : &str, second_part : bool) -> i32 {
    let input_sequence = input.trim().split(",");
    let mut hex : Hex = Hex::new();
    let mut max_distance_ever = 0;
    for direction in input_sequence {
        hex.step(direction);
        if second_part {
            let dist = hex.distance_from_origin();
            if dist > max_distance_ever {
                max_distance_ever = dist;
            }
        }
    }
    if second_part { max_distance_ever }
    else { hex.distance_from_origin() }
}

/// May we imagine a hexagonal tiling as having 3 axis that cross the corners of a hexagon
/// Z like /, Y like \, X like -
/// Steps in a direction:
/// north = X, +Y, -Z
/// south = X, -Y, +Z
/// north east = +X, Y, -Z
/// south west = -X, Y, +Z
/// South east = +X, -Y, Z
/// north west = -X, +Y, Z
#[derive(Debug)]
struct Hex {
    x : i32,
    y : i32,
    z : i32,
}

impl Hex {
    fn new() -> Hex {
        Hex { x: 0, y: 0, z:0}
    }

    fn distance_from_origin(&self) -> i32 {
        cmp::max(cmp::max(self.x.abs(),self.y.abs()),self.z.abs())
    }

    /// Moves one step in the direction provided
    /// Valid directions are n,ne,nw,s,se,sw
    fn step(&mut self, direction : &str) {
        match direction {
        "n" => { self.z -= 1; self.y +=1 },
        "s" => { self.z += 1; self.y -= 1 },
        "ne" => { self.x += 1; self.z -= 1 },
        "sw" => { self.x -= 1; self.z += 1 },
        "se" => { self.x += 1; self.y -= 1 },
        "nw" => { self.x -= 1; self.y += 1 },
        _ => panic!("Invalid input coordinate {}", direction),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test1_1() {
        assert_eq!(3, advent11_1("ne,ne,ne"));
    }

    #[test]
    fn test1_2() {
        assert_eq!(0, advent11_1("ne,ne,sw,sw"));
    }

    #[test]
    fn test1_3() {
        assert_eq!(2, advent11_1("ne,ne,s,s"));
    }

    #[test]
    fn test1_4() {
        assert_eq!(3, advent11_1("se,sw,se,sw,sw"));
    }

    #[test]
    fn test1_5() {
        assert_eq!(2, advent11_1("ne,se"));
    }
}