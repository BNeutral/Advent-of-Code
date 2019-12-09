from collections import defaultdict
import re
from queue import Queue

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

def part1(data):
	interp = Interpreter(data,[1])
	interp.runProgram()
	return list(interp.output.queue)

def part2(data):
	interp = Interpreter(data,[2])
	interp.runProgram()
	return list(interp.output.queue)
	

class Interpreter:

	#array is an array of ints contains the program 
	#inp is the input as an array
	def __init__(self, array, inp, useDefaultInput=True):
		self.array = array.copy()
		self.inputs = Queue()
		for i in inp:
			self.inputs.put(i)
		self.defaultInput = array[-1]
		self.useDefaultInput = useDefaultInput
		if useDefaultInput:
			self.output = Queue()
		else:
			self.output = None
		self.relativeBase = 0

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
			9:self.opAdjustBase,
			99:self.opHalt
		}
		pc = 0
		while True:
			opcode,modes = self.parseOpcodeAndModes(pc)
			newpc = ops[opcode](pc,modes)
			if newpc == -1:
				return
			pc = newpc

	def getInput(self):
		if self.useDefaultInput:
			try:
				a = self.inputs.get(False)
				return a
			except:
				return self.defaultInput
		else:
			return self.inputs.get()

	def opAdd(self, pc, modes):
		self.write(pc+3, modes[2], self.read(pc+1,modes[0]) + self.read(pc+2,modes[1]))
		return pc+4

	def opMul(self, pc, modes):
		self.write(pc+3, modes[2], self.read(pc+1,modes[0]) * self.read(pc+2,modes[1]))
		return pc+4

	def opInput(self, pc, modes):
		self.write(pc+1, modes[0], self.getInput())
		return pc+2

	def opOutput(self, pc, modes):
		self.output.put(self.read(pc+1,modes[0]))
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

	def opAdjustBase(self, pc, modes):
		self.relativeBase += self.read(pc+1,modes[0])
		return pc+2

	def parseOpcodeAndModes(self,pc):
		instruction = self.array[pc]
		opcode = instruction % 100
		modes = [0,0,0]
		for x in range(len(modes)):
			modes[x] = (instruction//pow(10,2+x)) % 10
		return opcode,modes

	def checkSize(self,index,mode):
		self.makeIndexValid(index)
		if mode == 0:
			self.makeIndexValid(self.array[index])
		elif mode == 2:
			self.makeIndexValid(self.array[index]+self.relativeBase)

	def makeIndexValid(self,index):
		size = len(self.array)
		if index >= size:
			dif = index - len(self.array) + 1
			self.array.extend([0]*dif)

	def read(self, index, mode):
		self.checkSize(index,mode)
		if mode == 0:
			return self.array[self.array[index]]
		elif mode == 1:
			return self.array[index]
		elif mode == 2:
			return self.array[self.array[index]+self.relativeBase]

	def write(self, index, mode, value):
		self.checkSize(index,mode)
		if mode == 0:
			self.array[self.array[index]] = value
		elif mode == 1:
			self.array[index] = value
		elif mode == 2:
			self.array[self.array[index]+self.relativeBase] = value

#Execution stuff

def test1():
	inp = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
	interp = Interpreter(dataToParsedArray(inp),[])
	interp.runProgram()
	print(list(interp.output.queue))
	inp = "1102,34915192,34915192,7,4,7,99,0"
	interp = Interpreter(dataToParsedArray(inp),[])
	interp.runProgram()
	print(list(interp.output.queue))
	inp = "104,1125899906842624,99"
	interp = Interpreter(dataToParsedArray(inp),[])
	interp.runProgram()
	print(list(interp.output.queue))
	return

def main():
	rawInput = open("./input/9.txt").read()
	data = dataToParsedArray(rawInput)
	print(part1(data))
	print(part2(data))
	return

#test1()
main()

#Python reminders
#range(start, end+1, step), len
#{}, for k in dict, for k,v in dict.items(), for v in dict.values()  
#set(), .add(x), .remove(x), .discard(x) no error if missing, x in s, |= union, &= intersect, -= difference, .copy()
#[], .append(), .insert(i,x), .pop([i]), .remove(x), .reverse(), sort(arr) in place, sorted(arr) new arr 
#map(single param function, list)
#filter(single param boolean returning function, list)
#reduce(2 param function, list)
#lambda x: x**2
#// integer division in python3
#sys.maxsize
#common global functions: abs() max() min() len()
#from queue import Queue ->thread safe, can be blocking, .put() .get()
#from threading import Thread ->thread = Thread(target = f). .start(), .join()
#from itertools import permutations -> permutations(list)
#from types import SimpleNamespace -> objet style = SimpleNamespace(**dict)	