use a10;
use std::fmt;
use std::collections::HashSet;

#[allow(dead_code)]
pub fn advent14_1(input : &str) -> u32 {
    let disk = Disk::from_input(input);
    disk.count_filled_cell()
}

#[allow(dead_code)]
pub fn advent14_2(input : &str) -> u32 {
    let disk = Disk::from_input(input);
    disk.count_groups()
}

const DISK_SIZE : usize = 128;

/// Represents a 128x128 bit region
struct Disk {
    data : Vec<Vec<u8>>,
}


impl Disk {
    /// Creates a new disk from the input as explained in the problem
    fn from_input(input : &str) -> Disk {
        let mut high = true;
        let mut num: u8 = 0;
        let mut disk = Disk { data : Vec::new() };
        for row in 0..DISK_SIZE { // Fill the disk vector
            let mut key = String::from(input);
            key.push_str("-");
            key.push_str(row.to_string().as_str());
            disk.data.push(Vec::new());
            let hash = a10::advent10_2(&key);
            for char in hash.chars() {
                let hex = char.to_digit(16).unwrap() as u8;
                if high {
                    num = hex << 4;
                    high = false;
                } else {
                    num |= hex;
                    disk.data[row].push(num);
                    high = true;
                }
            }
        }
        disk
    }

    /// Returns the amount of occupied bits
    fn count_filled_cell(&self) -> u32 {
        let mut filled_cells = 0;
        for row in &self.data {
            for byte in row {
                filled_cells += byte.count_ones();
            }
        }
        filled_cells
    }

    /// Returns the amount of separate islands
    fn count_groups(&self) -> u32 {
        let mut visited : HashSet<(i16,i16)> = HashSet::new();
        let mut group_counter : u32 = 0;
        for y in 0..DISK_SIZE {
            for x in 0..DISK_SIZE {
                if self.get_bit(x,y) {
                    if !visited.contains(&(x as i16,y as i16)) {
                        self.flood_fill(x as i16, y as i16, &mut visited);
                        group_counter += 1;
                    }
                }

            }
        }
        group_counter
    }

    fn flood_fill(&self, x : i16, y : i16, visited : &mut HashSet<(i16,i16)>) {
        if x < 0 || x >= DISK_SIZE as i16 || y < 0 || y >= DISK_SIZE as i16
            ||  visited.contains(&(x,y)) || !self.get_bit(x as usize,y as usize) {
            return
        }
        visited.insert((x,y));
        self.flood_fill(x-1, y, visited);
        self.flood_fill(x+1, y, visited);
        self.flood_fill(x,y-1, visited);
        self.flood_fill(x,y+1, visited);
    }

    /// Returns if a specific bit is on or off
    fn get_bit(&self, x : usize, y : usize) -> bool {
        let byte_offset = x / 8;
        let cmp : u8 = 0b10000000 >> (x % 8);
        self.data[y][byte_offset] & cmp > 0
    }
}

#[allow(unused_must_use)]
impl fmt::Display for Disk {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        for row in &self.data {
            for byte in row {
                for x in 0..8
                    {
                        if byte & (0b10000000 >> x) > 0 {
                            write!(f,"#");
                        }
                        else {
                            write!(f,".");
                        }
                    }
            }
            write!(f, "\n");
        }
        write!(f, "\n")
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test1_1() {
        assert_eq!(8108, advent14_1("flqrgnkx"));
    }

    #[test]
    fn test2_1() {
        assert_eq!(1242, advent14_2("flqrgnkx"));
    }

}