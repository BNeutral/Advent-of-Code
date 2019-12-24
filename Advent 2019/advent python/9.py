from queue import Queue
from util import *
from intcode import Interpreter

#Problem code

def part1(data):
	interp = Interpreter(data,[1])
	interp.runProgram()
	return list(interp.output.queue)

def part2(data):
	interp = Interpreter(data,[2])
	interp.runProgram()
	return list(interp.output.queue)
	
#Execution stuff

def test1():
	inp = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
	interp = Interpreter(commaSeparatedLineToInts(inp),[])
	interp.runProgram()
	print(list(interp.output.queue))
	inp = "1102,34915192,34915192,7,4,7,99,0"
	interp = Interpreter(commaSeparatedLineToInts(inp),[])
	interp.runProgram()
	print(list(interp.output.queue))
	inp = "104,1125899906842624,99"
	interp = Interpreter(commaSeparatedLineToInts(inp),[])
	interp.runProgram()
	print(list(interp.output.queue))
	return

def main():
	rawInput = open("./input/9.txt").read()
	data = commaSeparatedLineToInts(rawInput)
	print(part1(data))
	print(part2(data))
	return

#test1()
main()