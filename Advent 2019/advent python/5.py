from intcode import Interpreter
from util import *

def part1(data):
	program = Interpreter(data,[1])
	program.runProgram()
	out = program.output.get()
	while out == 0:
		out = program.output.get()
	print(out)

def part2(data):
	program = Interpreter(data,[5])
	program.runProgram()
	print(program.output.get())

#Execution stuff

def test2():
	rawInput = "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
	data = commaSeparatedLineToInts(rawInput)
	program = Interpreter(data,[7])
	program.runProgram()
	print(program.output.get())
	program = Interpreter(data,[8])
	program.runProgram()
	print(program.output.get())
	program = Interpreter(data,[9])
	program.runProgram()
	print(program.output.get())
	return

def main():
	rawInput = open("./input/5.txt").read()
	data = commaSeparatedLineToInts(rawInput)
	part1(data.copy())
	part2(data.copy())
	return

#test2()
main()