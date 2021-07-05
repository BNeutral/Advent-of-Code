from collections import defaultdict
from util import *
import re

#File parsing stuff
def dataToParsedArray(stringData) :
	result = [] 
	for line in stringData.split("\n"):
		line = line.strip()
		if line != "":
			result.append(parse(line))
	return Geology(result)

def parse(line) :
	mapLine = []
	for char in line:
		if char == ".":
			mapLine.append(0)
		elif char == "#":
			mapLine.append(1)
	return mapLine

#Problem code

def part1(data):
	return data.countForSlope(3,1)


def part2(data):
	mult = 1
	for (x,y) in [(1,1),(3,1),(5,1),(7,1),(1,2)]:
		mult *= data.countForSlope(x,y)
	return mult

class Geology:

	def __init__(self, geo):
		self.geo = geo
		self.height = len(geo)

	def isTree(self, x, y):
		row = self.geo[y]
		cell = row[x % len(row)]
		return cell == 1

	def countForSlope(self, slopeX, slopeY):
		x = 0
		y = 0
		treeCounter = 0
		while y < self.height:
			x += slopeX
			y += slopeY
			if y < self.height and self.isTree(x,y):
				treeCounter += 1
		return treeCounter

#Execution stuff

def test1():
	rawInput = "..##.......\n#...#...#..\n.#....#..#.\n..#.#...#.#\n.#...##..#.\n..#.##.....\n.#.#.#....#\n.#........#\n#.##...#...\n#...##....#\n.#..#...#.#\n"
	data = dataToParsedArray(rawInput)
	print(part1(data))
	return

def test2():
	rawInput = "..##.......\n#...#...#..\n.#....#..#.\n..#.#...#.#\n.#...##..#.\n..#.##.....\n.#.#.#....#\n.#........#\n#.##...#...\n#...##....#\n.#..#...#.#\n"
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