extern crate regex;
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
mod a18_1;
mod a18_2;
mod a19;

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
    let mut s = read_input("./input/input18");
	println!("{:?}", a18_2::advent18_2(&s));
}
