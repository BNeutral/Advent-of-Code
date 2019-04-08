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

def part1(data):
	constellations = []
	for point in data:
		constellations.append(Constellation([point]))
	oldLen = -1
	while oldLen != len(constellations):
		oldLen = len(constellations)
		x = 0
		while x < len(constellations):
			y = x+1
			const1 = constellations[x]
			while y < len(constellations):
				const2 = constellations[y]
				if const1.inDistance(const2):
					const1.combine(const2)
					idx = constellations.index(const2)
					del constellations[idx]
					if idx < y:
						y -= 1
				y += 1
			x += 1
	return len(constellations)

class Constellation:

	def __init__(self, pointArray):
		self.points = set(pointArray)

	def inDistance(self,other):
		for point1 in self.points:
			for point2 in other.points:
				if point1.distance(point2) <= 3:
					return True
		return False

	def combine(self, other):
		self.points |= other.points

	def __repr__(self):
		return str(self.points)

class Point:

	def __init__(self, string):
		self.coords = map(int, string.split(","))

	def distance(self, other):
		result = 0
		for x in range(len(self.coords)):
			result += abs(self.coords[x]-other.coords[x])
		return result

	def __repr__(self):
		return str(self.__dict__)

	def __eq__(self, other):
		return self.coords == other.coords

	def __hash__(self):
		return hash(tuple(self.coords))

#Execution stuff

def test1():
	rawInput = "0,0,0,0\n 3,0,0,0\n 0,3,0,0\n 0,0,3,0\n 0,0,0,3\n 0,0,0,6\n 9,0,0,0\n12,0,0,0"
	data = dataToParsedArray(rawInput)
	print(part1(data))
	return

def test2():
	rawInput = "-1,2,2,0\n0,0,2,-2\n0,0,0,-2\n-1,2,0,0\n-2,-2,-2,2\n3,0,2,-1\n-1,3,2,2\n-1,0,-1,0\n0,2,1,-2\n3,0,0,0"
	data = dataToParsedArray(rawInput)
	print(part1(data))
	return

def main():
	rawInput = open("./input/25.txt").read()
	data = dataToParsedArray(rawInput)
	print(part1(data))
	return

#test1()
#test2()
main()