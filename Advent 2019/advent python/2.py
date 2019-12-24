from intcode import Interpreter
from util import *

#Problem code

def part1(data):
	data[1] = 12
	data[2] = 2
	program = Interpreter(data)
	program.runProgram()
	return program.array[0]

def part2(data, target):
	for x in range(0,100):
		for y in range(0,100):
			newData = data.copy()
			newData[1] = x
			newData[2] = y
			program = Interpreter(newData)
			program.runProgram()
			if program.array[0] == target:
				return 100*x+y

#Execution stuff

def test1():
	rawInput = "1,9,10,3,2,3,11,0,99,30,40,50"
	data = commaSeparatedLineToInts(rawInput)
	program = Interpreter(data)
	program.runProgram()
	print(program.array[0])
	return

def main():
	rawInput = open("./input/2.txt").read()
	data = commaSeparatedLineToInts(rawInput)
	print(part1(data.copy()))
	print(part2(data.copy(), 19690720))
	return

#test1()
main()