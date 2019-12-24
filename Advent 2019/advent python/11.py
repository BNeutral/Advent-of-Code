from collections import defaultdict
from util import *
from queue import Empty
from threading import Thread
import sys
from intcode import Interpreter

#Problem code

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
	print("Computing...")
	print(part1(data))
	print(part2(data))
	return

main()