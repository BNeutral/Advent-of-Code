import re
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
	return Point(line)

#Problem code

def findMinMax(data):
	minX = sys.maxint
	maxX = -sys.maxint
	minY = sys.maxint
	maxY = -sys.maxint
	maxSpeed = -sys.maxint
	for point in data:
		minX = min(minX,point.x)
		maxX = max(maxX,point.x)
		minY = min(minY,point.y)
		maxY = max(maxY,point.y)
		maxSpeed = max(maxSpeed, abs(point.vx), abs(point.vy))
	return minX,maxX,minY,maxY,maxSpeed

def findMaxLength(minX,maxX,minY,maxY):
	return max(maxX-minX, maxY-minY)

def findMinMaxLength(minX,maxX,minY,maxY):
	return min(maxX-minX, maxY-minY)

def printPoints(data, minX, minY, maxX, maxY):
	canvas = [[' ' for _ in range(maxX-minX+1)] for _ in range(maxY-minY+1)]
	for point in data:
		canvas[point.y-minY][point.x-minX] = '#'
	for y in canvas:
		for x in y:
			sys.stdout.write(x)
		sys.stdout.write('\n')
		sys.stdout.flush()

def part1and2(data):
	counter = 0
	prevLen = sys.maxint
	while True:
		minX,maxX,minY,maxY,maxSpeed = findMinMax(data)
		maxLen = findMaxLength(minX,maxX,minY,maxY)
		if maxLen > prevLen:
			counter-=1
			for point in data:
				point.multipUpdate(-1)
			minX,maxX,minY,maxY,maxSpeed = findMinMax(data)
			print("Seconds elpased: "+str(counter))
			printPoints(data, minX, minY, maxX, maxY)
			break
		else:
			#A poorly thought optimization
			movement = max(1,findMinMaxLength(minX,maxX,minY,maxY)/3/maxSpeed)
			for point in data:
				point.multipUpdate(movement)
			counter += movement
			prevLen = maxLen
	return

class Point:

	def __init__(self, string):
		regex = re.compile(r'^position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>$')
		match = regex.match(string)
		self.x = int(match.group(1))
		self.y = int(match.group(2))
		self.vx = int(match.group(3))
		self.vy = int(match.group(4))

	def update(self):
		self.x += self.vx
		self.y += self.vy

	def multipUpdate(self, multiplier):
		self.x += self.vx * multiplier
		self.y += self.vy * multiplier

#Execution stuff

def test1():
	string = "position=< 9,  1> velocity=< 0,  2>\nposition=< 7,  0> velocity=<-1,  0>\nposition=< 3, -2> velocity=<-1,  1>\nposition=< 6, 10> velocity=<-2, -1>\nposition=< 2, -4> velocity=< 2,  2>\nposition=<-6, 10> velocity=< 2, -2>\nposition=< 1,  8> velocity=< 1, -1>\nposition=< 1,  7> velocity=< 1,  0>\nposition=<-3, 11> velocity=< 1, -2>\nposition=< 7,  6> velocity=<-1, -1>\nposition=<-2,  3> velocity=< 1,  0>\nposition=<-4,  3> velocity=< 2,  0>\nposition=<10, -3> velocity=<-1,  1>\nposition=< 5, 11> velocity=< 1, -2>\nposition=< 4,  7> velocity=< 0, -1>\nposition=< 8, -2> velocity=< 0,  1>\nposition=<15,  0> velocity=<-2,  0>\nposition=< 1,  6> velocity=< 1,  0>\nposition=< 8,  9> velocity=< 0, -1>\nposition=< 3,  3> velocity=<-1,  1>\nposition=< 0,  5> velocity=< 0, -1>\nposition=<-2,  2> velocity=< 2,  0>\nposition=< 5, -2> velocity=< 1,  2>\nposition=< 1,  4> velocity=< 2,  1>\nposition=<-2,  7> velocity=< 2, -2>\nposition=< 3,  6> velocity=<-1, -1>\nposition=< 5,  0> velocity=< 1,  0>\nposition=<-6,  0> velocity=< 2,  0>\nposition=< 5,  9> velocity=< 1, -2>\nposition=<14,  7> velocity=<-2,  0>\nposition=<-3,  6> velocity=< 2, -1>"
	data = dataToParsedArray(string)
	part1and2(data)
	return

def main():
	rawInput = open("./input/10.txt").read()
	data = dataToParsedArray(rawInput)
	part1and2(data)
	return

test1()
main()
