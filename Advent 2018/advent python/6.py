import re

#File parsing stuff
def dataToParsedArray(stringData) :
	result = [] 
	for line in stringData.split("\n"):
		line = line.strip()
		if line != "":
			result.append(parse(line))
	return result

def parse(line) :
	return Point(line)

#Problem code

def findMax(data):
	maxCoord = 0
	for point in data:
		maxCoord = max(maxCoord,point.x, point.y)
	return maxCoord

def paintGrid(data, grid):
	for x in range(len(grid)):
		for y in range(len(grid)):
			distances = []
			minD = 99999
			minID = -1
			for point in data:
				distance = point.distance(x,y)
				distances.append(distance)
				if distance < minD:
					minD = distance
					minID = point.id
			if distances.count(minD) > 1:
				minID = -1
			grid[y][x] = minID

def assignArea(data, grid):
	maxCoord = len(grid)-1
	for x in range(maxCoord+1):
		for y in range(maxCoord+1):
			value = grid[y][x]
			if value > 0:
				if data[value-1].area == -1:
					continue
				elif x == 0 or y == 0 or x == maxCoord or y == maxCoord:
					data[value-1].area = -1
				else:
					data[value-1].area += 1

def getMaxArea(data):
	areaSize = 0
	for point in data:
		if point.area > areaSize:
			areaSize = point.area
	return areaSize

def paintGridByDistance(data, grid, distance):
	counter = 0
	for x in range(len(grid)):
		for y in range(len(grid)):
			sum = 0
			for point in data:
				sum += point.distance(x,y)
			if sum < distance:
				counter +=1
	return counter

def part1(data):
	maxCoord = findMax(data)+1
	grid = [[0 for _ in range(maxCoord)] for _ in range(maxCoord)]
	paintGrid(data,grid)
	assignArea(data,grid)
	return getMaxArea(data)

def part2(data, distance):
	maxCoord = findMax(data)+1
	grid = [[0 for _ in range(maxCoord)] for _ in range(maxCoord)]
	return paintGridByDistance(data, grid, distance)

class Point:

	idCounter = 1

	def __init__(self, string):
		regex = re.compile(r'^(\d+), (\d+)$')
		match = regex.match(string)
		self.x = int(match.group(1))
		self.y = int(match.group(2))
		self.id = Point.idCounter
		self.area = 0
		Point.idCounter+=1

	def distance(self, x, y):
		return abs(x-self.x)+abs(y-self.y)
		
	def __repr__(self):
		return str(self.__dict__)

#Execution stuff

def test1():
	text = "1, 1\n1, 6\n8, 3\n3, 4\n5, 5\n8, 9"
	data = dataToParsedArray(text)
	print(part1(data))
	return

def test2():
	text = "1, 1\n1, 6\n8, 3\n3, 4\n5, 5\n8, 9"
	data = dataToParsedArray(text)
	print(part2(data, 32))
	return

def main():
	rawInput = open("./input/6.txt").read()
	data = dataToParsedArray(rawInput)
	print(part2(data, 10000))
	return

main()
