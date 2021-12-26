extern crate regex;
mod aoc;
mod a1;
mod a2;
mod a3;
mod a4;
mod a5;
mod a6;
mod a7;
mod a8;
mod a9;
mod a10;
mod a11;
mod a12;
mod a13;
mod a14;
mod a15;
mod a16;
mod a17;
mod a18;
//mod a18_2;
mod a19;
mod a20;
mod a21;
mod a22;
mod a23;
mod a24;
mod a25;

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
    let mut s = read_input("../input/25.txt");
	a25::day25(&s);
}
