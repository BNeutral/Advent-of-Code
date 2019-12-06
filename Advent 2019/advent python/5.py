from collections import defaultdict
import re

#File parsing stuff
def dataToParsedArray(stringData) :
	result = [] 
	for line in stringData.split(","):
		line = line.strip()
		if line != "":
			result.append(parse(line))
	return result

def parse(line) :
	return int(line)

#Problem code

# Class that runs the program
class Interpreter:

	#array is an array of ints contains the program 
	#inp is the input
	def __init__(self, array, inp):
		self.array = array
		self.input = inp

	def __repr__(self):
		return str(self.__dict__)

	def runProgram(self):
		ops = {
			1:self.opAdd,
			2:self.opMul,
			3:self.opInput,
			4:self.opOutput,
			5:self.opJmpTrue,
			6:self.opJmpFalse,
			7:self.opLessThan,
			8:self.opEquals,
			99:self.opHalt
		}
		pc = 0
		while True:
			opcode,modes = self.parseOpcodeAndModes(pc)
			newpc = ops[opcode](pc,modes)
			if newpc == -1:
				return
			pc = newpc

	def opAdd(self, pc, modes):
		self.write(pc+3, modes[2], self.read(pc+1,modes[0]) + self.read(pc+2,modes[1]))
		return pc+4

	def opMul(self, pc, modes):
		self.write(pc+3, modes[2], self.read(pc+1,modes[0]) * self.read(pc+2,modes[1]))
		return pc+4

	def opInput(self, pc, modes):
		self.write(pc+3, modes[2], self.input)
		return pc+2

	def opOutput(self, pc, modes):
		print(self.read(pc+1,modes[0]))
		return pc+2

	def opJmpTrue(self, pc, modes):
		if self.read(pc+1, modes[0]) != 0:
			return self.read(pc+2, modes[1])
		return pc+3

	def opJmpFalse(self, pc, modes):
		if self.read(pc+1, modes[0]) == 0:
			return self.read(pc+2, modes[1])
		return pc+3

	def opLessThan(self, pc, modes):
		if self.read(pc+1,modes[0]) < self.read(pc+2,modes[1]):
			self.write(pc+3, modes[2],1)
		else:
			self.write(pc+3, modes[2],0)
		return pc+4

	def opEquals(self, pc, modes):
		if self.read(pc+1,modes[0]) == self.read(pc+2,modes[1]):
			self.write(pc+3, modes[2],1)
		else:
			self.write(pc+3, modes[2],0)
		return pc+4

	def opHalt(self, pc, modes):
		return -1

	def parseOpcodeAndModes(self,pc):
		instruction = self.array[pc]
		opcode = instruction % 100
		modes = [0,0,0]
		for x in range(len(modes)):
			modes[x] = (instruction//pow(10,2+x)) % 10
		return opcode,modes

	def read(self, index, mode):
		if mode == 0:
			return self.array[self.array[index]]
		elif mode == 1:
			return self.array[index]

	def write(self, index, mode, value):
		if mode == 0:
			self.array[self.array[index]] = value
		elif mode == 1:
			self.array[index] = value


def part1(data):
	Interpreter(data,1).runProgram()

def part2(data):
	Interpreter(data,5).runProgram()

#Execution stuff

def test2():
	rawInput = "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
	data = dataToParsedArray(rawInput)
	Interpreter(data,7).runProgram()
	Interpreter(data,8).runProgram()
	Interpreter(data,9).runProgram()
	return

def main():
	rawInput = open("./input/5.txt").read()
	data = dataToParsedArray(rawInput)
	part1(data.copy())
	part2(data.copy())
	return

#test2()
main()