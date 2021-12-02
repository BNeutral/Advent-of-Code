extern crate regex;
mod aoc;
mod a1;
mod a2;

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
    let mut s = read_input("../input/1.txt");
	a1::day1(&s);
}
