extern crate regex;
mod aoc;
mod a1;
mod a2;
mod a3;

use std::fs::File;
use std::io::prelude::*;

#[allow(dead_code)]
fn read_input(path : &str) -> String {
	let mut file : File = File::open(path).unwrap();
	let mut contents : String = String::new();
	file.read_to_string(&mut contents).unwrap();
	contents
}

#[allow(unused_mut)]
fn main() {
    let mut s = read_input("../input/3.txt");
	a3::day3(&s);
}
