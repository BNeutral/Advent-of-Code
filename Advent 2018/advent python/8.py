#File parsing stuff
def dataToParsedArray(stringData) :
	result = [] 
	for line in stringData.split(" "):
		line = line.strip()
		if line != "":
			result.append(parse(line))
	return result

def parse(line) :
	return int(line)

#Problem code
def part1(data):
	return Tree(data).getValue1()


def part2(data):
	return Tree(data).getValue2()

class Tree:

	def __init__(self, array):
		self.root = Node()
		self.root.parse(array)

	def getValue1(self):
		return self.root.value1()

	def getValue2(self):
		return self.root.value2()

	def __repr__(self):
		return str(self.__dict__)

class Node:

	def __init__(self):
		self.childCount = 0
		self.children = []
		self.metaCount = 0
		self.meta = []

	def parse(self, array):
		self.childCount = array[0]
		self.metaCount = array[1]
		offset = 2
		for _ in range(self.childCount):	
			node = Node()
			self.children.append(node)
			offset += node.parse(array[offset:])
		length = offset + self.metaCount
		self.meta = array[0:length][-self.metaCount:]
		return length

	def value1(self):
		counter = sum(self.meta)
		for child in self.children:
			counter += child.value1()
		return counter

	def value2(self):
		if self.childCount == 0:
			return sum(self.meta)
		else:
			counter = 0
			for index in self.meta:
				if index <= len(self.children):
					counter += self.children[index-1].value2()
			return counter

	def __repr__(self):
		return str(self.__dict__)

#Execution stuff

def test1():
	inp = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
	data = dataToParsedArray(inp)
	print(part1(data))
	return

def test2():
	inp = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
	data = dataToParsedArray(inp)
	print(part2(data))
	return

def main():
	rawInput = open("./input/8.txt").read()
	data = dataToParsedArray(rawInput)
	print(part1(data))
	print(part2(data))
	return

main()
