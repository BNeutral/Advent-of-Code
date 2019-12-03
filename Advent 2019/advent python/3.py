from collections import defaultdict
import re
import sys

#File parsing stuff
def dataToParsedArray(stringData) :
	wires = []
	data = stringData.split("\n")
	for line in data:
		wires.append(line.split(","))
	return wires

#Problem code

def part1(data):
	return problem(data)

def part2(data):
	return problem(data,False)

def norm(tuple):
	return abs(tuple[0])+abs(tuple[1])

def manhattanDistance(tuple1,tuple2):
	return abs(tuple1[0]-tuple2[0])+abs(tuple1[1]-tuple2[1])

def problem(data, part1=True):
	letterLut = {"U":(0,1),"D":(0,-1),"L":(-1,0),"R":(1,0)}
	intersections = set()
	points = []
	distances = []
	for wire in data:
		wirePoints = set()
		wirePoints.add((0,0))
		points.append(wirePoints)
	for wire in data:
		distances.append({})
	currentWire = 0
	for wire in data:
		x = 0
		y = 0
		distanceSoFar = 0
		for segment in wire:
			letter = segment[0]
			distance = int(segment[1:])
			for _ in range(distance):
				distanceSoFar += 1
				lut = letterLut[letter]
				x += lut[0]
				y += lut[1]
				for z in range(len(points)):
					if z != currentWire and (x,y) in points[z]:
						intersections.add((x,y))
				points[currentWire].add((x,y))
				hasDist = distances[currentWire].get((x,y))
				if hasDist:
					distances[currentWire][(x,y)] = min(distanceSoFar,hasDist)
				else:
					distances[currentWire][(x,y)] = distanceSoFar
		currentWire += 1
	maxDist = sys.maxsize
	for point in intersections:
		if part1 == True:
			maxDist = min(norm(point),maxDist)
		else:
			total = 0
			for z in range(len(points)):
				total += distances[z][point]
			maxDist = min(total, maxDist)
	return maxDist

#Execution stuff

def test1():
	rawInput = "R8,U5,L5,D3\nU7,R6,D4,L4"
	data = dataToParsedArray(rawInput)
	print(part1(data))
	rawInput = "R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83"
	data = dataToParsedArray(rawInput)
	print(part1(data))
	rawInput ="R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
	data = dataToParsedArray(rawInput)
	print(part1(data))
	return

def test2():
	rawInput = "R8,U5,L5,D3\nU7,R6,D4,L4"
	data = dataToParsedArray(rawInput)
	print(part2(data))
	rawInput = "R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83"
	data = dataToParsedArray(rawInput)
	print(part2(data))
	rawInput ="R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
	data = dataToParsedArray(rawInput)
	print(part2(data))
	return

def main():
	rawInput = open("./input/3.txt").read()
	data = dataToParsedArray(rawInput)
	print(part1(data))
	print(part2(data))
	return

#test1()
#test2()
main()