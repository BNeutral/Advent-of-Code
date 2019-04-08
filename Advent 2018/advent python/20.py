import sys

#Problem code

def solve(string):
	gridDict = traverse(string)
	#printMap(gridDict)	
	distances, maxDist, over1k = findDistances(gridDict)
	return maxDist, over1k

def printMap(gridDict):
	minX, maxX, minY, maxY = findMinMaxes(gridDict)
	for y in range(minY-1,maxY+2):
		for x in range(minX-1, maxX+2):
			pos = Position(x,y)
			if pos in gridDict:
				sys.stdout.write(str(gridDict[pos]))
			else:
				sys.stdout.write("#")
		sys.stdout.write("\n")
		sys.stdout.flush()
	sys.stdout.flush()

def findMinMaxes(gridDict):
	minX = sys.maxint
	maxX = 0
	minY = sys.maxint
	maxY = 0
	for key in gridDict:
		minX = min(minX, key.x)
		maxX = max (maxX, key.x)
		minY = min(minY, key.y)
		maxY = max(maxY, key.y)
	return minX, maxX, minY, maxY

def findDistances(gridDict):
	toVisit = [Position(0,0)]
	distances = {}
	distances[toVisit[0]] = 0
	doneSpace = set()
	maxDist = 0
	over1k = 0
	while len(toVisit) > 0:
		space = toVisit[0]
		currentDistance = distances[space]
		adjacents = space.freeAdjacentPositions(gridDict)
		for adj in adjacents:
			if adj not in doneSpace and adj not in toVisit:
				dist = currentDistance
				if (gridDict[adj] == "."):
					dist += 1
					if dist >= 1000:
						over1k += 1
				distances[adj] = dist
				toVisit.append(adj)
				maxDist = max(maxDist, dist)
		doneSpace.add(space)
		toVisit.remove(space)
	return distances, maxDist, over1k

class Position:

	def __init__(self, x, y):
		self.x = x
		self.y = y

	#Returns the sum of two positions as a new Position
	def add(self, other):
		return Position(self.x + other.x, self.y + other.y)

	def up(self):
		return self.add(Position(0,-1))

	def down(self):
		return self.add(Position(0,1))

	def right(self):
		return self.add(Position(1,0))

	def left(self):
		return self.add(Position(-1,0))

	def freeAdjacentPositions(self, gridDict):
		positions = []
		for pos in [self.up(), self.left(), self.right(), self.down()]:
			if pos in gridDict:
				positions.append(pos)
		return positions

	def __repr__(self):
		return str(self.__dict__)

	def __hash__(self):
		return hash( (self.x,self.y) )

	def __eq__(self, another):
		return self.x == another.x and self.y == another.y

#^N(EEE|WWW)NN(E|W)S$
# 1|        |2|2  |4
def traverse(string):
	gridDict = { Position(0,0) : "X" }
	currentPositions = set([Position(0,0)])
	startPositions = [set() for _ in range(1024)]
	endPositions = [set() for _ in range(1024)]
	parenCounter = 0
	for char in string:
		if char == "(":
			parenCounter += 1
			startPositions[parenCounter] = set(currentPositions)
			endPositions[parenCounter] = set()
		elif char == "|":
			endPositions[parenCounter] |= currentPositions
			currentPositions = set(startPositions[parenCounter])
		elif char == ")":
			endPositions[parenCounter] |= currentPositions
			currentPositions = set(endPositions[parenCounter])
			parenCounter -= 1
		elif char in "NEWS":
			new = set()
			for pos in currentPositions:
				new.add(addToDict(pos, char, gridDict))
			currentPositions = new
	return gridDict
	
def addToDict(position, char, gridDict):
	fun = { "N" : Position.up, "S" : Position.down, "E" : Position.right, "W" : Position.left}
	position = fun[char](position)
	gridDict[position] = "+"
	position = fun[char](position)
	gridDict[position] = "."
	return position
	

#Execution stuff

def test1():
	print "Test 0"
	printMap(traverse("^N(EEE|WWW)NN(EE|WW)(N|S)$"))
	print "Test 1"
	printMap(traverse("^ENWWW(NEEE|SSE(EE|N))$"))
	print "Test 2"
	printMap(traverse("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"))
	print "Test 3"
	printMap(traverse("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$"))
	print "Test 4"
	printMap(traverse("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$"))
	print "Test == 23"
	print(part1("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$"))
	print "Test == 31"
	print(part1("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$"))
	return

def main():
	rawInput = open("./input/20.txt").read()
	print(solve(rawInput))
	return

#test1()
main()
