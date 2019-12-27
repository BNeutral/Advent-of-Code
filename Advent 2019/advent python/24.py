from util import *
import copy

#File parsing stuff
def dataToParsedArray(stringData) :
	result = [] 
	for line in stringData.split("\n"):
		result.append([])
		line = line.strip()
		for char in line:
			if char == "." or char == "?":
				result[-1].append(0)
			else:
				result[-1].append(1)
	return result

#Problem code

def part1(data):
	seen = set()
	while True:
		newMap = nextMap(data)
		diversity = bioHash(newMap)
		if diversity in seen:
			return diversity
		seen.add(diversity)
		data = newMap

def bioHash(data):
	height = len(data)
	width = len(data[0])
	counter = 0
	for x in range(height*width):
		y = x // height
		counter += data[y][x%width] << x
	return counter

def nextMap(data):
	height = len(data)
	width = len(data[0])
	newMap = copy.deepcopy(data)
	for y in range(height):
		for x in range(width):
			adjacentBugs = 0
			for adj in Vector2(x,y).fourAdjacents():
				if adj.x < 0 or adj.x >= width or adj.y < 0 or adj.y >= height:
					continue
				else:
					adjacentBugs += data[adj.y][adj.x]
			if data[y][x] == 1 and adjacentBugs != 1:
				newMap[y][x] = 0
			elif data[y][x] == 0 and (adjacentBugs == 1 or adjacentBugs == 2):
				newMap[y][x] = 1
	return newMap

#Levels outside : -1
#Levels inside : +1
#We'll just check a bunch of empty levels since the problem is small enough
def part2(data, iterations=200):
	levels = {}
	levels[0] = copy.deepcopy(data)
	levels[-1] = emptyGrid()
	levels[1] = emptyGrid()
	bugs = 0
	print("Simulating...")
	for x in range(iterations):
		#print(x)
		levels, bugs = nextMap3D(levels)
	return bugs

def emptyGrid(size=3):
	grid = []
	for _ in range(5):
		grid.append([])
		for _ in range(5):
			grid[-1].append(0)
	return grid	

def getLevelPos(levels, level, y, x):
	if level in levels:
		return levels[level][y][x]
	return 0

def getLevelPosBugs(levels, level, y, x, fromY, fromX):
	if x < 0:
		return getLevelPos(levels, level-1,2,1)
	elif x > 4:
		return getLevelPos(levels,level-1,2,3)
	elif y < 0:
		return getLevelPos(levels,level-1,1,2)
	elif y > 4:
		return getLevelPos(levels,level-1,3,2)
	elif x == 2 and y == 2:
		if level+1 not in levels:
			return 0
		if fromX == 2:
			if fromY == 1:
				return sum(levels[level+1][0])
			elif fromY == 3:
				return sum(levels[level+1][4])
		elif fromY == 2:
			if fromX == 1:
				return verticalSum(levels[level+1],0)
			elif fromX == 3:
				return verticalSum(levels[level+1],4)
	else:
		return getLevelPos(levels,level,y,x)

def verticalSum(array2D, column):
	s = 0
	for y in range(5):
		s += array2D[y][column]
	return s

def nextMap3D(levels):
	bugs = 0
	newMap = copy.deepcopy(levels)
	for level in levels.keys():
		for y in range(5):
			for x in range(5):
				if y == 2 and x == 2:
					continue
				adjacentBugs = 0
				for adj in Vector2(x,y).fourAdjacents():
					adjacentBugs += getLevelPosBugs(levels, level, adj.y, adj.x, y, x)
				if levels[level][y][x] == 1 and adjacentBugs != 1:
					newMap[level][y][x] = 0
				elif levels[level][y][x] == 0 and (adjacentBugs == 1 or adjacentBugs == 2):
					newMap[level][y][x] = 1
					bugs += 1
				elif levels[level][y][x] == 1:
					bugs += 1
				if newMap[level][y][x] == 1:
					if y == 1 or y == 3 or x == 1 or x == 3:
						if level+1 not in newMap:
							newMap[level+1] = emptyGrid()
					if y == 0 or y == 4 or x == 0 or x == 4:
						if level-1 not in newMap:
							newMap[level-1] = emptyGrid()
	return newMap, bugs

#Execution stuff

def test1():
	rawInput = "....#\n#..#.\n#..##\n..#..\n#...."
	step = dataToParsedArray(rawInput)
	for _ in range(4):
		step = nextMap(step)
		print("-")
		for line in step:
			print(line)
	print(part1(dataToParsedArray(rawInput)) == 2129920)
	return

def test2():
	rawInput = "....#\n#..#.\n#.?##\n..#..\n#....\n"
	data = dataToParsedArray(rawInput)
	print(part2(data, 10) )
	return

def main():
	rawInput = open("./input/24.txt").read()
	data = dataToParsedArray(rawInput)
	print(part1(data))
	print(part2(data))
	return

#test1()
#test2()
main()