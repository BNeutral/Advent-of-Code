import sys

#File parsing stuff
def inputParse(stringData) :
	units = []
	grid = []
	y = 0
	for line in stringData.split("\n"):
		line = line.strip()
		if line != "":
			parse(line, units, grid, y)
		y += 1
	return units, grid

#Parses a line
def parse(line, units, grid, y) :
	row = []
	grid.append(row)
	x = 0
	for char in line:
		if char == "#":
			row.append("#")
		elif char == ".":
			row.append(".")
		else: #Goblin or elf
			row.append(Unit(x,y,units,grid,char))
		x += 1


#Problem code

#Prints the grid without units
def printGrid(grid):
	for y in grid:
		for x in y:
			sys.stdout.write(str(x))
		sys.stdout.write("\n")
		sys.stdout.flush()
	sys.stdout.flush()

#Prints the grid with whatever is passed in dictionary where key=Position
def printGridOverlayed(grid, dictionary):
	for y in range(len(grid)):
		for x in range(len(grid[y])):
			pos = Position(x,y)
			if pos in dictionary:
				sys.stdout.write(str(dictionary[pos]))
			else:
				sys.stdout.write(str(grid[y][x]))
		sys.stdout.write("\n")
		sys.stdout.flush()
	sys.stdout.flush()

#Prints the health of the units
def printHealhts(units):
	for unit in units:
		print unit.unitType+str(unit.hitPoints)

def part1(units, grid):
	return simulate(units, grid, False)

#Simulates the game
def simulate(units, grid, abortOnElfDeath):
	goOn =True
	turnCount = 0
	aliveCounter = { "G" : 0, "E" : 0}
	for unit in units:
		aliveCounter[unit.unitType] += 1
	startingElves = aliveCounter["E"]
	while goOn:
		turnCount += 1
		units.sort()
		i = 0
		while i < len(units):
			unit = units[i]
			target = unit.update()
			if target and target.hitPoints <= 0:
				index = units.index(target)
				target.die()
				aliveCounter[target.unitType] -= 1
				if abortOnElfDeath and aliveCounter["E"] < startingElves:
					return None
				if aliveCounter["G"] <= 0 or aliveCounter["E"] <= 0:
					goOn = False
					if i < len(units): #Last turn wasn't completed
						turnCount -= 1
					break
				if index > i:
					i += 1				
			else:
				i += 1
		#print(turnCount)
		#printGrid(grid)
		#printHealhts(units)
	hpSum = sum(unit.hitPoints for unit in units)
	return turnCount*hpSum

def part2(rawInput):
	units, grid = inputParse(rawInput)
	elfPower = 4
	adjustElfPower(units, elfPower)
	result = simulate(units, grid, True)
	while not result:
		elfPower += 1
		units, grid = inputParse(rawInput)
		adjustElfPower(units, elfPower)
		result = simulate(units, grid, True)
	return result,elfPower

#Changes the elf power for a group of units
def adjustElfPower(units, power):
	for unit in units:
		if unit.unitType == 'E':
			unit.attackPower = power
			
class Position:

	def __init__(self, x, y):
		self.x = x
		self.y = y

	#Returns the sum of two positions as a new Position
	def add(self, other):
		return Position(self.x + other.x, self.y + other.y)

	#Returns the Manhattan distance to another Position
	def distance(self, other):
		return abs(self.x-other.x)+abs(self.y-other.y)

	#Returns the positions that are adjacent to this position
	def adjacentPositions(self):
		positions = []
		for pos in [Position(0, -1) , Position(-1, 0) , Position(1, 0) , Position(0, 1)]:
			positions.append(self.add(pos))
		return positions

	#Returns the positions that are free and ajacent to this position
	def freeAdjacentPositions(self, grid):
		positions = []
		for pos in [Position(0, -1) , Position(-1, 0) , Position(1, 0) , Position(0, 1)]:
			pos.x += self.x
			pos.y += self.y
			occupant = grid[pos.y][pos.x]
			if str(occupant) == ".":
				positions.append(pos)
		return positions

	#Find min distances from current position in a poorly optimized way
	def findDistances(self, grid):
		toVisit = [self]
		distances = {}
		distances[toVisit[0]] = 0
		doneSpace = set()
		while len(toVisit) > 0:
			space = toVisit[0]
			currentDistance = distances[space]
			adjacents = space.freeAdjacentPositions(grid)
			for adj in adjacents:
				if adj not in doneSpace and adj not in toVisit:
					dist = currentDistance + 1
					distances[adj] = dist
					toVisit.append(adj)
			doneSpace.add(space)
			toVisit.remove(space)
		return distances

	def __hash__(self):
		return hash((self.x,self.y))

	def __str__(self):
		return str(self.x)+","+str(self.y)

	def __cmp__(self, other):
		if self.y != other.y:
			if self.y < other.y:
				return -1
			else:
				return 1
		elif self.x != other.x:
			if self.x < other.x:
				return -1
			else:
				return 1
		else:
			return 0

class Unit:

	#Initializes. Adds itself to the unit list
	def __init__(self, x, y, units, grid, unitType):
		self.position = Position(x,y)
		self.hitPoints = 200
		self.attackPower = 3
		self.grid = grid
		self.units = units
		self.units.append(self)
		self.unitType = unitType

	#Makes a unit perform the actions for the turn
	def update(self):
		possibleTargets = self.identifyTargets()
		adjacentTargets = self.checkForAdjacentTarget(possibleTargets)
		if not adjacentTargets:
			reachable = self.findSpacesInRange(possibleTargets)
			targetTile = self.findMovement(reachable)
			if targetTile:
				self.move(targetTile)	
			else:
				return
		adjacentTargets = self.checkForAdjacentTarget(possibleTargets)
		if not adjacentTargets:
			return	
		adjacentTargets.sort(key = lambda unit: (unit.hitPoints, unit.position))
		target = adjacentTargets[0]
		self.attack(target)
		return target

	#Returns all possible targets
	def identifyTargets(self):
		#possibleTargets = list(filter(lambda unit: unit.unitType != self.unitType, self.units))
		possibleTargets = []
		for unit in self.units:
			if unit.unitType != self.unitType:
				possibleTargets.append(unit)
		return possibleTargets

	#Returns the manhattan distance between two units
	def distance(self, other):
		return self.position.distance(other.position)

	#Returns array of targets if already next to targets
	def checkForAdjacentTarget(self, possibleTargets):
		adjacents = []
		for target in possibleTargets:
			if self.distance(target) <= 1:
				adjacents.append(target)
		return adjacents

	#Given a list of enemies, finds all spaces next to enemies that are free. 
	#The so called "in range" spaces
	def findSpacesInRange(self, enemies):
		spaces = []
		for enemy in enemies:
			spaces.extend(enemy.freeAdjacentPositions())
		return spaces

	#Returns an array of all positions that are free next to this unit
	def freeAdjacentPositions(self):
		return self.position.freeAdjacentPositions(self.grid)

	#Given a list of spaces, returns the space where it should move. Could be optimized a ton
	def findMovement(self, spaces):
		distances = self.position.findDistances(self.grid)
		targetSpace = self.findClosest(distances, spaces)
		if not targetSpace:
			return
		#Find where to move by recalculating
		distances = targetSpace.findDistances(self.grid)
		movementOptions = []
		minDistWalk = sys.maxint
		for pos in self.position.freeAdjacentPositions(self.grid):
			if pos in distances:
				distToTarget = distances[pos]
				if distToTarget < minDistWalk:
					minDistWalk = distToTarget
					movementOptions = [pos]
				elif distToTarget == minDistWalk:
					movementOptions.append(pos)
		if not movementOptions:
			return []
		else:
			movementOptions.sort()
			return movementOptions[0]

	#Given distances returns the space that meets the closeness criteria
	def findClosest(self, distances, spaces):
		minDist = sys.maxint
		possibleTargetSpaces = []
		for space in spaces:
			if space in distances:
				distance = distances[space]
				if distance < minDist:
					possibleTargetSpaces = [space]
					minDist = distance
				if distance == minDist:
					possibleTargetSpaces.append(space)
		possibleTargetSpaces.sort()
		if not possibleTargetSpaces:
			return None
		return possibleTargetSpaces[0]

	#Moves to target tile and updates grid
	def move(self, newPosition):
		self.editGridPos(".")
		self.position = newPosition
		self.editGridPos(self)

	#Deals Damage
	def attack(self, enemy):
		#print self.unitType+" is attacking "+enemy.unitType+" at "+str(enemy.position)
		enemy.receiveDamage(self.attackPower)

	#Receives damage. Death check done externally
	def receiveDamage(self, attackPower):
		self.hitPoints -= attackPower

	#Dies
	def die(self):
		self.units.remove(self)
		self.editGridPos(".")

	#Changes the grid to this new thing
	def editGridPos(self, newThing):
		self.grid[self.position.y][self.position.x] = newThing

	def __str__(self):
		return self.unitType

	def __repr__(self):
		return self.unitType

	def __cmp__(self, other):
		return self.position.__cmp__(other.position)

#Execution stuff

def battleTest1(rawInput, expectedNumber):
	units, grid = inputParse(rawInput)
	#printGrid(grid)
	print(part1(units,grid),"<-"+str(expectedNumber))

def battleTest2(rawInput, expectedNumbers):
	#printGrid(grid)
	print(part2(rawInput),"<-"+str(expectedNumbers))

def test1():
	rawInput = "#######\n#.G...#\n#...EG#\n#.#.#G#\n#..G#E#\n#.....#\n#######\n"
	battleTest1(rawInput,27730)
	rawInput = "#######\n#G..#E#\n#E#E.E#\n#G.##.#\n#...#E#\n#...E.#\n#######\n"
	battleTest1(rawInput,36334)
	rawInput = "#######\n#E..EG#\n#.#G.E#\n#E.##E#\n#G..#.#\n#..E#.#\n#######\n"
	battleTest1(rawInput,39514)
	rawInput = "#######\n#.E...#\n#.#..G#\n#.###.#\n#E#G#G#\n#...#G#\n#######\n"
	battleTest1(rawInput,28944)
	rawInput = "#########\n#G......#\n#.E.#...#\n#..##..G#\n#...##..#\n#...#...#\n#.G...G.#\n#.....G.#\n#########\n"
	battleTest1(rawInput,18740)
	return

def test2():
	rawInput = "#######\n#.G...#\n#...EG#\n#.#.#G#\n#..G#E#\n#.....#\n#######\n"
	battleTest2(rawInput,(15,4988))
	rawInput = "#######\n#G..#E#\n#E#E.E#\n#G.##.#\n#...#E#\n#...E.#\n#######\n"
	battleTest2(rawInput,(4,29064))
	rawInput = "#######\n#E..EG#\n#.#G.E#\n#E.##E#\n#G..#.#\n#..E#.#\n#######\n"
	battleTest2(rawInput,(4,31284))
	rawInput = "#######\n#.E...#\n#.#..G#\n#.###.#\n#E#G#G#\n#...#G#\n#######\n"
	battleTest2(rawInput,(12,6474))
	rawInput = "#########\n#G......#\n#.E.#...#\n#..##..G#\n#...##..#\n#...#...#\n#.G...G.#\n#.....G.#\n#########\n"
	battleTest2(rawInput,(34,1140))
	return

def main():
	rawInput = open("./input/15.txt","r").read()
	units,grid = inputParse(rawInput)
	printGrid(grid)
	print(part2(rawInput))
	return

test1()
test2()
main()
