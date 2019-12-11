from collections import defaultdict
from util import *
import re
from queue import Queue,Empty
from threading import Thread
import sys

#Problem code

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
		self.output = Queue()
		self.relativeBase = 0
		self.isRunning = False

	def __repr__(self):
		return str(self.__dict__)

	def runProgram(self):
		self.isRunning = True
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
				self.isRunning = False
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

def part1(data):
	robot = Robot(data)
	robot.run()
	return robot.countPaintedPanels()

def part2(data):
	robot = Robot(data)
	robot.run(1)
	return robot.drawPanels()

class Robot:

	turnLeftLut = {
		Vector2(0,1) : Vector2(1,0),
		Vector2(1,0) : Vector2(0,-1),
		Vector2(0,-1) : Vector2(-1,0),
		Vector2(-1,0) : Vector2(0,1),
		}

	turnRightLut = {
		Vector2(0,1) : Vector2(-1,0),
		Vector2(1,0) : Vector2(0,1),
		Vector2(0,-1) : Vector2(1,0),
		Vector2(-1,0) : Vector2(0,-1),
		}

	def __init__(self, program):
		self.program = Interpreter(program, [], False)
		self.input = self.program.inputs
		self.direction = Vector2(0,-1)
		self.position = Vector2(0,0)
		self.panels = defaultdict(int)

	def parseOutput(self):
		try:
			self.panels[self.position] = self.program.output.get(timeout=10)
			rotation = self.program.output.get(timeout=1)
			if rotation == 0: #turn left
				self.direction = Robot.turnLeftLut[self.direction]
			elif rotation == 1:
				self.direction = Robot.turnRightLut[self.direction]
			self.position = self.position.add(self.direction)
		except Empty:
			return #Ignored since only timout case should be after the program finished running


	def run(self, initialPaint=0):
		self.panels[self.position] = initialPaint
		self.program.isRunning = True
		thread = Thread(target = self.program.runProgram)
		thread.start()
		while self.program.isRunning:
			self.input.put(self.panels[self.position])
			self.parseOutput()
		thread.join()

	def drawPanels(self):
		printchars = ["░", "▓", " "]
		minx = sys.maxsize
		maxx = -sys.maxsize
		miny = sys.maxsize
		maxy = -sys.maxsize
		for vector in self.panels.keys():
			minx = min(vector.x,minx)
			miny = min(vector.y,minx)
			maxx = max(vector.x,maxx)
			maxy = max(vector.y,maxy)
		width = maxx - minx
		height = maxy - miny
		result = ""
		for y in range(miny,maxy+1):
			for x in range(minx,maxx+1):
				pos = Vector2(x,y)
				if pos in self.panels:
					result += printchars[self.panels[pos]]
				else:
					result += printchars[2]
			result += "\n"
		return result	

	def countPaintedPanels(self):
		return len(self.panels.keys())

#Execution stuff

def main():
	rawInput = open("./input/11.txt").read()
	data = commaSeparatedLineToInts(rawInput)
	print(part1(data))
	print(part2(data))
	return

main()

#Python reminders
#range(start, end+1, step), len
#{}, for k in dict, for k,v in dict.items(), for v in dict.values()  
#set(), .add(x), .remove(x), .discard(x) no error if missing, x in s, |= union, &= intersect, -= difference, .copy()
#[], .append(), .insert(i,x), .pop([i]), .remove(x), .reverse(), sort(arr) in place, sorted(arr) new arr 
#heap: heapq lib, heappush(list, value), heappop(list), value can be a tuple and gets sorted by 1st item
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