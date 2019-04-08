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
	return Rectangle(line)

#Problem solving code
def part1(data, fabric):
	for rectangle in data:
		rectangle.cover(fabric)
	counter = 0
	for y in range(0,len(fabric)):
		for x in range(0,len(fabric[y])):
			if fabric[x][y] > 1:
				counter += 1
	return counter


def part2(data, fabric):
	for rectangle in data:
		rectangle.cover(fabric)
	for rectangle in data:
		if rectangle.doesntOverlap(fabric):
			return rectangle.id

class Rectangle:

	def __init__(self, string):
		regex = re.compile(r'^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$')
		match = regex.match(string)
		self.id = int(match.group(1))
		self.x = int(match.group(2))
		self.y = int(match.group(3))
		self.width = int(match.group(4))
		self.height = int(match.group(5))

	def cover(self, fabric):
		x = self.x
		y = self.y
		for x in range(self.x, self.x + self.width):
			for y in range(self.y, self.y + self.height):
				fabric[x][y] += 1
		return

	def doesntOverlap(self, fabric):
		x = self.x
		y = self.y
		for x in range(self.x, self.x + self.width):
			for y in range(self.y, self.y + self.height):
				if fabric[x][y] > 1 :
					return False
		return True

	def __repr__(self):
		return 'id:{} x:{} y:{} width:{} height:{}'.format(self.id,self.x,self.y,self.width,self.height)

#Execution stuff
def test1():
	data = "#123 @ 3,2: 5x4"
	print(Rectangle(data))
	return

#TODO: Use an Enum
def main():
	fabric = [[0 for _ in range(1000)] for _ in range(1000)]
	rawInput = open("./input/3.txt").read()
	data = dataToParsedArray(rawInput)
	print(part2(data,fabric))
	return

main()
