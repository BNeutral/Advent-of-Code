from collections import defaultdict
import re
import math
from util import Vector2
from heapq import heappush,heappop

#File parsing stuff
def dataToAsteroids(stringData) :
	fullMap = []
	onlyAsteroids = set()
	y = 0
	for line in stringData.split("\n"):
		fullMap.append([])
		x = 0
		for character in line:
			if character == ".":
				fullMap[-1].append(None)
			elif character == "#":
				asteroid = Asteroid(x,y,fullMap,onlyAsteroids)
				fullMap[-1].append(asteroid)
				onlyAsteroids.add(asteroid)
			x += 1
		y += 1
	return onlyAsteroids

#Problem code

def part1(rawInput):
	asteroids = dataToAsteroids(rawInput)
	maxVisible = 0
	ast = None
	for asteroid in asteroids:
		visible = asteroid.countVisible()
		if visible > maxVisible:
			maxVisible = visible
			ast = asteroid
	return maxVisible, ast.position.x, ast.position.y


def part2(rawInput, stationX, stationY):
	asteroids = dataToAsteroids(rawInput)
	anAsteroid = asteroids.pop()
	asteroids.add(anAsteroid)
	baseAsteroid = anAsteroid.fullMap[stationY][stationX]
	return baseAsteroid.vaporize200()

class Asteroid:

	def __init__(self, x, y, fullMap, onlyAsteroids):
		self.position = Vector2(x,y)
		self.fullMap = fullMap
		self.onlyAsteroids = onlyAsteroids

	# Basically checks for "non reversed" colinearity (as in, 1,1 colinear with 2,2 but not with -1,-1)
	# Puts colinear things the same arrays, then counts how many arrays we ended up with
	def countVisible(self):
		toVisit = self.onlyAsteroids.copy()
		toVisit.remove(self)
		colinearSets = []
		for asteroid in toVisit:
			direction = asteroid.position.sub(self.position)
			added = False
			for aSet in colinearSets:
				if aSet[0].isSameDirectionColinear(direction):
					added = True
					aSet.append(direction)
			if not added:
				colinearSets.append([direction])
		return len(colinearSets)

	# Similar to the step before, puts all same direction colinear asteroids in arrays
	# Then sorts the arrays by distance, then sorts the clump of arrays by angle
	# Picks one of each (as to go clockwise) until it destroys 200 
	def vaporize200(self):
		toVisit = self.onlyAsteroids.copy()
		toVisit.remove(self)
		colinearSets = []
		counter = 0
		for asteroid in toVisit:
			direction = asteroid.position.sub(self.position)
			distance = direction.length()
			angle = direction.angle()
			added = False
			for aSet in colinearSets:
				if aSet[0][2].isSameDirectionColinear(direction):
					added = True
					aSet.append( (distance,angle,direction, asteroid) )
			if not added:
				colinearSets.append([ (distance,angle,direction, asteroid) ])
		for array in colinearSets:
			array.sort(key=lambda x: x[0])
		colinearSets.sort(key=lambda x: x[0][2].angle(), reverse=True)
		while True:
			for array in colinearSets:
				if len(array) > 0:
					asteroid = array.pop(0)[3]
					counter += 1
					if counter == 200:
						return asteroid.position.x*100+asteroid.position.y

	def __repr__(self):
		return "#"

#Execution stuff

def linearTest():
	print(Vector2(1,0).isSameDirectionColinear(Vector2(-1,0))) #No
	print(Vector2(1,1).isSameDirectionColinear(Vector2(-1,-1))) #No
	print(Vector2(1,1).isSameDirectionColinear(Vector2(0.5,0.5))) #Yes
	print(Vector2(-1,1).isSameDirectionColinear(Vector2(-1,-1))) #No
	print(Vector2(12,12).isSameDirectionColinear(Vector2(1,1))) #Yes
	print(Vector2(0.1,-0.5).isSameDirectionColinear(Vector2(1,-5))) #Yes

def test1():
	rawInput = "......#.#.\n#..#.#....\n..#######.\n.#.#.###..\n.#..#.....\n..#....#.#\n#..#....#.\n.##.#..###\n##...#..#.\n.#....####"
	print(part1(rawInput),33)
	rawInput = "#.#...#.#.\n.###....#.\n.#....#...\n##.#.#.#.#\n....#.#.#.\n.##..###.#\n..#...##..\n..##....##\n......#...\n.####.###."
	print(part1(rawInput),35)
	rawInput = ".#..#..###\n####.###.#\n....###.#.\n..###.##.#\n##.##.#.#.\n....###..#\n..#.#..#.#\n#..#.#.###\n.##...##.#\n.....#.#..\n"
	print(part1(rawInput),41)
	rawInput = ".#..##.###...#######\n##.############..##.\n.#.######.########.#\n.###.#######.####.#.\n#####.##.#.##.###.##\n..#####..#.#########\n####################\n#.####....###.#.#.##\n##.#################\n#####.##.###..####..\n..######..##.#######\n####.##.####...##..#\n.#####..#.######.###\n##...#.##########...\n#.##########.#######\n.####.#.###.###.#.##\n....##.##.###..#####\n.#.#.###########.###\n#.#.#.#####.####.###\n###.##.####.##.#..##\n"
	print(part1(rawInput),210)
	return

def test2():
	rawInput = ".#..##.###...#######\n##.############..##.\n.#.######.########.#\n.###.#######.####.#.\n#####.##.#.##.###.##\n..#####..#.#########\n####################\n#.####....###.#.#.##\n##.#################\n#####.##.###..####..\n..######..##.#######\n####.##.####...##..#\n.#####..#.######.###\n##...#.##########...\n#.##########.#######\n.####.#.###.###.#.##\n....##.##.###..#####\n.#.#.###########.###\n#.#.#.#####.####.###\n###.##.####.##.#..##\n"
	print(part2(rawInput,11,13))
	return

def main():
	rawInput = open("./input/10.txt").read()
	visible, x, y = part1(rawInput)
	print(visible, x, y)
	print(part2(rawInput,x,y))
	return

#linearTest()
#test1()
#test2()
main()