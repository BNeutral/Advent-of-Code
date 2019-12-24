from util import *
from intcode import Interpreter
import re

#Problem code

def part1(data):
	program = Interpreter(data,[],False)
	thread = program.runInThread()
	output = getData(program, 2479)
	outputAsString = outputToString(output).strip()
	#print(outputAsString)
	splitOutput = outputAsString.split("\n")
	sumIntersections = 0
	height = len(splitOutput) - 1
	width = len(splitOutput[0]) - 1
	for y in range(height + 1):
		for x in range(width + 1):
			if hasScaffoldNeighbours(splitOutput, x, y, width, height):
				sumIntersections += (x*y)			
	return sumIntersections,splitOutput

def hasScaffoldNeighbours(splitOutput, x, y, width, height):
	tile = splitOutput[y][x]
	if tile != "#":
		return False
	if x <= 0 or x >= width or y <= 0 or y >= height:
		return False
	up = splitOutput[y-1][x] == "#"
	down = splitOutput[y+1][x] == "#"
	left = splitOutput[y][x-1] == "#"
	right = splitOutput[y][x+1] == "#"
	return up and down and left and right

#Reads the size expected, or if none is expected until it times out
def getData(program, size=0):
	output = []
	try:
		if size != 0:
			for _ in range(size):
				output.append(program.output.get())
		else:
			while True:
				output.append(program.output.get(timeout = 5))
	except:
		pass
	return output

#Turns the output array to ascii string
def outputToString(output):
	result = ""
	for x in output:
		result += str(chr(x))
	return result

def part2(data, maze):
	data[0] = 2
	program = Interpreter(data,[],False)
	thread = program.runInThread()
	inputs = figureOutInputs(maze)
	for inp in inputs:
		sendInput(program, inp)
	sendInput(program,"n")
	output = getData(program, 2479)
	output.extend(getData(program, 65))
	output = getData(program, 2480)
	outputAsString = outputToString(output).strip()
	#print(outputAsString)	
	#while program.isRunning:
	#	output = getData(program, 2479)
	#	outputAsString = outputToString(output).strip()
	#	print(outputAsString)
	return getData(program, 1).pop()

#Sends a string as ascii characters to the program
def sendInput(program,input):
	for char in input:
		program.inputs.put(ord(char))
	program.inputs.put(10)

#figures out the inputs
def figureOutInputs(maze):
	startingPos, startingCharacter, mazeAsDict = mazeToDict(maze)
	#print(drawDictScreen(mazeAsDict,["#"]))
	robot = Robot(startingPos, startingCharacter, mazeAsDict)
	stepArray = robot.simpleTraverse()
	return stepsToPattern(stepArray)

#Turns the maze into a dictionary with just the floor tiles
def mazeToDict(maze):
	mazeAsDict = {}
	startingPos = None
	startingCharacter = "^"
	for y in range(len(maze)):
		for x in range(len(maze[0])):
			tile = maze[y][x]
			if tile != ".":
				position = Vector2(x,y)
				mazeAsDict[position] = 0				
				if tile != "#":
					startingPos = position
					startingCharacter = tile
	return startingPos, startingCharacter, mazeAsDict

#Given an array of strings detailing each movement, use brute force to find the patterns
def stepsToPattern(stepArray):
	stringSteps = ",".join(stepArray)
	for x in range(20):
		for y in range(20):
			for z in range(20):
				patterns, success = dumbMatcher(stringSteps, [x,y,z])
				if success:
					letters = ["A", "B", "C"]
					for x in range(len(letters)):
						if patterns[x][0] == ",":
							patterns[x] = patterns[x][1:]
						stringSteps = stringSteps.replace(patterns[x],letters[x])
					result = [stringSteps]
					result.extend(patterns)
					return result	

#Find the sequence in a very dumb way
def dumbMatcher(stringSteps, sizes):
	patterns = []
	for x in range(len(sizes)):
		p = stringSteps[0:sizes[x]]
		patterns.append(p)
		stringSteps = stringSteps.replace(p, "")
	stringSteps = stringSteps.replace(",", "")
	return patterns, stringSteps==""

#Class for traversing the maze
class Robot:

	facingDic = {
		"^" : Vector2.up,
		"<" : Vector2.left,
		">" : Vector2.right,
		"v" : Vector2.down					
	}

	turnLeftLut = {
		Vector2.down : Vector2.right,
		Vector2.left : Vector2.down,
		Vector2.up  : Vector2.left ,
		Vector2.right  : Vector2.up,
	}

	turnRightLut = {
		Vector2.down : Vector2.left,
		Vector2.left : Vector2.up,
		Vector2.up  : Vector2.right ,
		Vector2.right  : Vector2.down,
	}

	def __init__(self, position, facingCharacter, mazeAsDict):
		self.position = position
		self.facing = Robot.facingDic[facingCharacter]
		self.maze = mazeAsDict
		self.totalToVisit = len(mazeAsDict)

	#We make some assumptions about what the correct traversal looks like
	#Namely that it only turns at corners
	def simpleTraverse(self):
		steps = []
		visited = set()
		visited.add(self.position)
		#drawDict = {}
		counter = 0
		while len(visited) < len(self.maze):
			if self.tryAdvance():
				self.position = self.position.add(self.facing)
				counter += 1
				visited.add(self.position)
				#drawDict[self.position] = str(counter%10)
				pass
			elif self.tryRotateLeft():
				if counter != 0:
					steps.append(str(counter))
				steps.append("L")
				#drawDict[self.position] = str("L")
				counter = 0
				self.facing = Robot.turnLeftLut[self.facing]
				pass
			elif self.tryRotateRight():
				if counter != 0:
					steps.append(str(counter))
				steps.append("R")
				#drawDict[self.position] = str("R")
				counter = 0
				self.facing = Robot.turnRightLut[self.facing]
				pass
		steps.append(str(counter))
		#print(drawDictScreenSimple(drawDict))
		#print(steps)
		return steps

	#Returns true if moving in the current facing would end in a floor tile
	def tryAdvance(self):
		nextPos = self.position.add(self.facing)
		return nextPos in self.maze

	#Returns true if moving after rotating left would end in a floor tile
	def tryRotateLeft(self):
		newFacing = Robot.turnLeftLut[self.facing]
		nextPos = self.position.add(newFacing)
		return nextPos in self.maze

	#Returns true if moving after rotating right would end in a floor tile
	def tryRotateRight(self):
		newFacing = Robot.turnRightLut[self.facing]
		nextPos = self.position.add(newFacing)
		return nextPos in self.maze

#Execution stuff

def main():
	rawInput = open("./input/17.txt").read()
	data = commaSeparatedLineToInts(rawInput)
	result,maze = part1(data)
	print(result)
	print(part2(data,maze))
	return

main()