from util import *
import copy
from intcode import Interpreter

def part1(data):
	program = Interpreter(data)
	program.runInThread()
	while True:
		print(program.getASCIIOutput(timeout=0.1))
		program.sendASCIIInput(input())

def main():
	rawInput = open("./input/25.txt").read()
	data = commaSeparatedLineToInts(rawInput)
	print(part1(data))
	return

main()
