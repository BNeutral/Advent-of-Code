static BLOCK_SIZE: usize = 16;

#[allow(dead_code)]
pub fn advent10_1(input : &str) -> u32 {
    let vec = knot_hash_1(&input);
    vec[0] as u32 * vec[1] as u32
}

#[allow(dead_code)]
pub fn advent10_2(input : &str) -> String {
    let vec = knot_hash_64(&input);
    to_dense_hash(&vec)
}

/// Applies the 256bit knot hash once
pub fn knot_hash_1(input : &str) -> Vec<u8> {
    let input = transform_input_1(input);
    knot_hash(&input, 255,1)
}

/// Applies the 256bit knot hash 64 times
pub fn knot_hash_64(input : &str) -> Vec<u8> {
    let input = transform_input_2(input);
    knot_hash(&input, 255,64)
}

/// Uses the input to return a hashed result, max size 256 bits
/// Input is a byte vector of numbers to use for the algorithm
/// len is the amount of bits-1 the hash should have, max 255
/// rounds is how many times to run the algorithm on the result
fn knot_hash(input : &Vec<u8>, len : u8, rounds: u8) -> Vec<u8> {
    let mut vector : Vec<u8> = gen_vec(0,len);
    let len = vector.len();
    let mut current_pos : usize = 0;
    let mut skip_size : usize = 0;
    for _ in 0..rounds {
        for length in input {
            let length = *length as usize;
            for x in 0..length / 2 { // Inversion logic
                let start_pos = (current_pos + x) % len;
                let end_pos = (current_pos + length - x - 1) % len;
                vector.swap(start_pos, end_pos);
            }
            current_pos = (current_pos + length + skip_size) % len;
            skip_size += 1;
        }
    }
    vector
}

/// Given a vector of u8s turns each batch of BLOCK_SIZE into a single u8
fn to_dense_hash(hash : &Vec<u8>) -> String {
    let mut start = 0;
    let mut end = BLOCK_SIZE;
    let mut result : String = String::new();
    while end <= hash.len() {
        let byte = xor_block(&hash[start..end]);
        result.push_str(format!("{:02x}", byte).as_str());
        start += BLOCK_SIZE;
        end += BLOCK_SIZE;
    }
    result
}

/// Returns the result of applying xors to a slice of BLOCK_SIZE size
fn xor_block(slice : &[u8]) -> u8 {
    let mut result = slice[0];
    for x in 1..BLOCK_SIZE {
        result ^= slice[x];
    }
    result
}

/// Transforms the input into the proper format for part 1
fn transform_input_1(input : &str) -> Vec<u8> {
    let result = input.trim().split(",").map(|s : &str| s.parse::<u8>().unwrap()).collect();
    result
}

/// Transforms the input into the proper format for part 2
fn transform_input_2(input : &str) -> Vec<u8> {
    let mut bytes : Vec<u8> = input.trim().bytes().collect();
    bytes.extend([17,31,73,47,23].iter());
    bytes
}


/// Creates a vector of [start start+1 ... end-1 end]
fn gen_vec(start : u8, end : u8) -> Vec<u8> {
    let mut vec : Vec<u8> = Vec::new();
    for i in start..end { //TODO: Make into an inclusive range when Rust updates
        vec.push(i);
    }
    vec.push(end);
    vec
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_gen() {
        assert_eq!(4,gen_vec(0, 4)[4]);
    }

    #[test]
    fn test_transform() {
        assert_eq!(vec![49,44,50,44,51,17,31,73,47,23],transform_input_2("1,2,3"));
    }

    #[test]
    fn test_xor() {
        assert_eq!(64,xor_block(&[65,27,9,1,4,3,40,50,91,7,6,0,2,5,68,22]));
    }


    #[test]
    fn test1_1() {
        let str = "3,4,1,5";
        let input = transform_input_1(str);
        let hash = knot_hash(&input, 4, 1);
        assert_eq!(12,hash[0]*hash[1]);
    }

    #[test]
    fn test2_1() {
        assert_eq!("a2582a3a0e66e6e86e3812dcb672a272",advent10_2(""));
    }

    #[test]
    fn test2_2() {
        assert_eq!("33efeb34ea91902bb2f59c9920caa6cd",advent10_2("AoC 2017"));
    }

    #[test]
    fn test2_3() {
        assert_eq!("3efbe78a8d82f29979031a4aa0b16a9d",advent10_2("1,2,3"));
    }

    #[test]
    fn test2_4() {
        assert_eq!("63960835bcdc130f0b66d7ff4f6a5a8e",advent10_2("1,2,4"));
    }

}
