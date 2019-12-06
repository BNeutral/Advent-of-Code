from collections import defaultdict
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
	return line

#Problem code

def part1(data):
	tracker = OrbitTracker()
	for line in data:
		tracker.addPlanet(line)
	return tracker.traverse()


def part2(data):
	tracker = OrbitTracker()
	for line in data:
		tracker.addPlanet(line)
	return tracker.traverse("YOU","SAN")

class OrbitTracker:

	def __init__(self):
		self.directOrbits = defaultdict(lambda: [])

	def addPlanet(self,string):
		split = string.split(")")
		first = split[0]
		second = split[1]
		self.directOrbits[first].append(second)
		self.directOrbits[second].append(first)

	def traverse(self, start="COM", end=None):
		counter = defaultdict(lambda: 0)
		visited = set()
		toVisit = set()
		toVisit.add(start)
		while len(toVisit) > 0:
			current = toVisit.pop()
			visited.add(current)
			for planet in self.directOrbits[current]:
				counter[planet] = counter[current] + 1
				if planet not in visited:
					toVisit.add(planet)
		if not end:
			return sum(counter.values())
		else:
			return counter[end] - 2

#Execution stuff

def test1():
	rawInput = "COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L"
	data = dataToParsedArray(rawInput)
	print(part1(data))
	return

def test2():
	rawInput = "COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L\nK)YOU\nI)SAN"
	data = dataToParsedArray(rawInput)
	print(part2(data))
	return

def main():
	rawInput = open("./input/6.txt").read()
	data = dataToParsedArray(rawInput)
	print(part1(data))
	print(part2(data))
	return

#test1()
#test2()
main()