import sys

#File parsing stuff
def dataToParsedArray(stringData) :
	result = [] 
	for line in stringData.split("\n"):
		line = line.strip()
		if line != "":
			result.append(parse(line))
	return result

def parse(line) :
	return Slice(line)

#Problem code

def solve(slices):
	grid, minX, minY = createGrid(slices)
	water = WaterSource(grid, minX)
	water.update()
	printGrid(grid)
	temporary = 0
	permanent = 0
	for y in range(minY, len(grid)):
		array = grid[y]
		temporary += array.count("|")
		permanent += array.count("~")
	return temporary+permanent,permanent

def createGrid(slices):
	minX, maxX, minY, maxY = findMinMaxes(slices)
	width = maxX - minX
	startXIndex = minX-1
	grid = [["." for _ in range(width+3)] for _ in range(maxY+1)]
	for sli in slices:
		for y in sli.y.toRange():
			for x in sli.x.toRange():
				grid[y][x-startXIndex] = "#"
	return grid, startXIndex, minY
				
#Prints the grid
def printGrid(grid):
	for y in grid:
		for x in y:
			sys.stdout.write(str(x))
		sys.stdout.write("\n")
		sys.stdout.flush()
	sys.stdout.flush()

def findMinMaxes(slices):
	minX = sys.maxint
	maxX = 0
	minY = sys.maxint
	maxY = 0
	for sli in slices:
		minX = min(minX, sli.x.start())
		maxX = max (maxX, sli.x.end())
		minY = min(minY, sli.y.start())
		maxY = max(maxY, sli.y.end())
	return minX, maxX, minY, maxY

class Values:

	def __init__(self, string):
		self.values = map(int, string.split(".."))

	def toRange(self):
		return range(self.start(), self.end()+1)

	def start(self):
		return self.values[0]

	def end(self):
		return self.values[-1]

	def __repr__(self):
		return str(self.__dict__)

class Slice:

	def __init__(self, string):
		string = string.replace(" ","")
		for substring in string.split(","):
			if substring[0] == "x":
				self.x = Values(substring[2:])
			else:
				self.y = Values(substring[2:])

	def __repr__(self):
		return str(self.__dict__)

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

	def __repr__(self):
		return str(self.__dict__)

class WaterSource:

	def __init__(self, grid, minX):
		self.position = Position(500-minX, 0)
		self.droplets = []
		self.grid = grid

	def update(self):
		droplet = WaterDroplet(self.position.add(Position(0,1)), self.grid)
		droplet.run()

	def __repr__(self):
		return str(self.__dict__)

class WaterDroplet:

	def __init__(self, position, grid):
		self.position = position
		self.splitPoints = []
		self.splitDirections = []
		self.direction = 0
		self.grid = grid
		self.editGridPos("|")
		self.alive = True 

	def run(self):
		while self.alive:			
			self.update()

	def canTraverseTile(self, position):
		tile = self.tileAtPos(position)
		return tile == "." or tile == "|"

	def update(self):
		if self.position.y >= len(self.grid)-1:
			self.die()
			return
		if self.direction == 0:
			pos = self.position.down()
			if self.canTraverseTile(pos):
				self.move(pos)
			else:
				self.split()
				self.die()
		else:
			pos = self.position.down()
			if self.canTraverseTile(pos):
				self.direction = 0				
				return
			if self.direction == -1:
				pos = self.position.left()
				if self.canTraverseTile(pos):
					self.move(pos)
				else:
					self.checkStagnation()
					self.die()
			else:
				pos = self.position.right()
				if self.canTraverseTile(pos):
					self.move(pos)
				else:
					self.checkStagnation()
					self.die()

	def fillStagnant(self):
		tile = self.tileAtPos(self.position)
		while tile != "#":
			self.editGridPos("~")
			if self.direction == 1:
				self.position = self.position.left()
			else:
				self.position = self.position.right()
			tile = self.tileAtPos(self.position)

	def checkStagnation(self):
		pos = self.position
		tile = self.tileAtPos(pos)
		while tile == "|" and not self.canTraverseTile(pos.down()):
			if self.direction == 1:
				pos = pos.left()
			else:
				pos = pos.right()
			tile = self.tileAtPos(pos)
			if tile == "#":
				self.fillStagnant()
				return

	#Kills the current droplet, returns to a previous point if it split
	def die(self):
		if self.splitPoints:
			self.position = self.splitPoints.pop()
			self.direction = self.splitDirections.pop()
		else:
			self.alive = False
		#printGrid(self.grid)

	def split(self):
		rightTile = self.tileAtPos(self.position.right())
		leftTile = self.tileAtPos(self.position.left())
		if (rightTile == "." or rightTile == "#") and (leftTile == "." or leftTile == "#"):
			self.splitPoints.append(self.position.up())
			self.splitDirections.append(0)
		self.splitPoints.append(self.position)
		self.splitDirections.append(-1)
		self.splitPoints.append(self.position)
		self.splitDirections.append(+1)

	def move(self, newPosition, symbol="|"):
		self.position = newPosition
		self.editGridPos(symbol)

	def tileAtPos(self, position):
		return self.grid[position.y][position.x]

	#Changes the grid symbol at the curren position
	def editGridPos(self, newThing):
		self.grid[self.position.y][self.position.x] = newThing

	def __repr__(self):
		return str(self.__dict__)

#Execution stuff

def test1():
	rawInput = "x=495, y=2..7\ny=7, x=495..501\nx=501, y=3..7\nx=498, y=2..4\nx=506, y=1..2\nx=498, y=10..13\nx=504, y=10..13\ny=13, x=498..504\n"
	slices = dataToParsedArray(rawInput)
	print(slices)
	print(findMinMaxes(slices))
	grid, minX, minY = createGrid(slices)
	printGrid(grid)
	print(solve(slices))
	return

def test2():
	rawInput = "x=495, y=2..7\ny=7, x=495..501\nx=501, y=3..7\nx=498, y=2..4\nx=506, y=1..2\n"
	rawInput = rawInput+"x=501, y=9..13\nx=503, y=9..12\ny=13, x=501..503\n"
	rawInput = rawInput+"x=490, y=16..25\nx=510, y=16..25\ny=25, x=490..510\n"
	rawInput = rawInput+"x=504, y=17..20\nx=508, y=17..20\ny=20, x=504..508\ny=17, x=504..508\n"
	rawInput = rawInput+"x=495, y=19..20\nx=500, y=15..25\ny=20, x=495..500\ny=19, x=495..500\n"
	slices = dataToParsedArray(rawInput)
	grid, minX, minY = createGrid(slices)
	printGrid(grid)
	print(solve(slices))
	return

def main():
	rawInput = open("./input/17.txt","r").read()
	slices = dataToParsedArray(rawInput)
	print(solve(slices))
	return

#test1()
#test2()
main()
