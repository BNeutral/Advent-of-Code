from util import *
from intcode import Interpreter
import random

#Problem code

def part1and2(data):
	program = Interpreter(data, [], False)
	thread = program.runInThread()
	program.isRunning = True
	controller = Controller(program)
	tileMap = controller.getMap()
	oxigen = controller.oxigen
	minutes = -1 #Start at -1 since firt iteration just adds the first to spawn
	visited = set()
	toVisit = set()
	toVisit.add(oxigen)
	while len(toVisit) > 0:
		nextVisit = set()
		while len(toVisit) > 0:
			node = toVisit.pop()
			visited.add(node)
			tileMap[node] = 2
			for vector in node.fourAdjacents():
				if tileMap[vector] == 1 and vector not in visited:
					nextVisit.add(vector)
		minutes += 1
		toVisit = nextVisit
		#print(drawDictScreen(tileMap, ["▓", ".","O"]))
	return controller.distanceToOxigen(),minutes

class Controller:

	directions = {
		1 : Vector2(0,-1),
		2 : Vector2(0,1),
		3 : Vector2(-1,0),
		4 : Vector2(1,0),
	}

	opposites = {
		1 : 2,
		2 : 1,
		3 : 4,
		4 : 3		
	}

	def __init__(self, program):
		self.program = program
		self.position = Vector2.zero
		self.nextInput = 1
		self.nextDirection = Controller.directions[1]
		self.drawMap = { self.position : 1 }
		self.oxigen = None
		self.inputStack = []
		self.distances = { Vector2.zero : 0}

	def getMap(self):
		self.addAdyacentToStack(self.position)
		while len(self.inputStack) > 0:
			nextInput = self.inputStack.pop()
			self.changeNext(nextInput)
			self.advance()
			#print(drawDictScreen(self.drawMap, ["▓", ".","O"], self.position))
		return self.drawMap

	def addAdyacentToStack(self, position):
		previousMove = None
		if len(self.inputStack) > 0:
			previousMove = Controller.opposites[self.nextInput]
		for inp in range(1,5):
			if inp != previousMove:
				newPos = position.add(Controller.directions[inp])
				if newPos not in self.drawMap:
					self.inputStack.append(inp)

	def nextPos(self):
		return self.position.add(self.nextDirection)
				
	def advance(self):
		currentPosDistance = self.distances[self.position]
		nextDistance = currentPosDistance+1
		nextPos = self.nextPos()
		self.program.inputs.put(self.nextInput)
		status = self.program.output.get()
		newVisit = nextPos in self.drawMap
		self.drawMap[nextPos] = status
		if nextPos in self.distances:
			self.distances[nextPos] = min(self.distances[nextPos], nextDistance)
		else:
			self.distances[nextPos] = nextDistance
		if status > 0:
			if status == 2:
				self.oxigen = nextPos
			self.position = nextPos
			if not newVisit:
				self.inputStack.append(Controller.opposites[self.nextInput])
				self.addAdyacentToStack(nextPos)

	def changeNext(self,inp):
		self.nextInput = inp
		self.nextDirection = Controller.directions[self.nextInput]

	def distanceToOxigen(self):
		return self.distances[self.oxigen]

#Execution stuff

def main():
	rawInput = open("./input/15.txt").read()
	data = commaSeparatedLineToInts(rawInput)
	p1,p2 = part1and2(data)
	print(p1)
	print(p2)
	return

main()