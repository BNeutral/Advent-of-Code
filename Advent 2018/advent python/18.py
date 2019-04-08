import sys
import copy

#Input
def inputParse(stringData) :
	grid = []
	for line in stringData.split("\n"):
		line = line.strip()
		if line != "":
			grid.append([char for char in line])
	return grid

#Problem code

def part2(grid):
	return part1(grid, 1000000000)

def part1(grid, iterations):
	modulus = 0
	results = set()
	for i in range(1,iterations+1):
		newGrid = copy.deepcopy(grid)
		lumberyards = 0
		wooded = 0
		for y in range(len(grid)):
			for x in range(len(grid[y])):
				tile = grid[y][x]
				if tile == ".":
					if countAdjacent(grid, x, y, "|") >= 3:
						newGrid[y][x] = "|"	
						wooded += 1					
				elif tile == "|":
					if countAdjacent(grid, x, y, "#") >= 3:
						newGrid[y][x] = "#"	
						lumberyards += 1
					else:
						wooded += 1					
				else: #Lumberyard
					if countAdjacent(grid, x, y, "#") == 0 or countAdjacent(grid, x, y, "|") == 0:
						newGrid[y][x] = "."	
					else:
						lumberyards += 1
				tile = newGrid[y][x]								
		grid = newGrid
		result = lumberyards*wooded
		if i > 1000: #TODO: Less arbitrary start of the loop detection
			if result in results:
				modulus = len(results)
				if i % modulus == 1000000000 % modulus:
					return result
			else:
				results.add(result)
	return result

def countAdjacent(grid, centerX, centerY, symbol):
	startX = max(0, centerX - 1)
	startY = max(0, centerY - 1)
	endX = min(centerX + 2, len(grid[0]) )
	endY = min(centerY + 2, len(grid) )
	counter = 0
	for y in range(startY, endY):
		for x in range(startX, endX):
			if x == centerX and y == centerY:
				continue
			elif grid[y][x] == symbol:
				counter += 1
	return counter

#Prints the grid
def printGrid(grid):
	for y in grid:
		for x in y:
			sys.stdout.write(str(x))
		sys.stdout.write("\n")
		sys.stdout.flush()
	sys.stdout.flush()

class Class:

	classVar = 1

	def __init__(self, string):
		regex = re.compile(r'^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$')
		match = regex.match(string)
		self.p1 = int(match.group(1))

	def aFunction(self):
		print("{0}".format(self.param))

	def __iter__(self):
		return self

	def __next__(self):
		return self

	def __repr__(self):
		return str(self.__dict__)

#Execution stuff

def test0():
	grid = [["|","|","|"],["|","|","|"],[".","#","#"]]
	print countAdjacent(grid, 1, 1, "|")
	print countAdjacent(grid, 1, 1, "#")
	print countAdjacent(grid, 1, 1, ".")


def test1():
	rawInput = ".#.#...|#.\n.....#|##|\n.|..|...#.\n..|#.....#\n#.#|||#|#|\n...#.||...\n.|....|...\n||...#|.#|\n|.||||..|.\n...#.|..|."
	grid = inputParse(rawInput)
	printGrid(grid)
	print(part1(grid,10))
	printGrid(grid)
	return

def main():
	rawInput = open("./input/18.txt","r").read()
	grid = inputParse(rawInput)
	#printGrid(grid)
	print(part1(grid,10))
	print(part2(grid))
	return

#test0()
#test1()
main()
