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
	return


def part2(data):
	return

class Class:

	classVar = 1

	def __init__(self, string):
		regex = re.compile(r'^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$')
		match = regex.match(string)
		self.p1 = int(match.group(1))

	def aFunction(self):
		print("{0}".format(self.param))

	def __iter__(self):
		return self

	def __next__(self):
		return self

	def __eq__(self, other):
		return self.p1 == other.p1

	def __repr__(self):
		return str(self.__dict__)

	def __hash__(self):
		return hash( (self.p1,self.p2) )

#Execution stuff

def test1():
	rawInput = ""
	data = dataToParsedArray(rawInput)
	print(part1(data))
	return

def test2():
	rawInput = ""
	data = dataToParsedArray(rawInput)
	print(part2(data))
	return

def main():
	rawInput = open("./input/1.txt").read()
	data = dataToParsedArray(rawInput)
	print(part1(data))
	return
main()
