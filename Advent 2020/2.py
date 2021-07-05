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
	return result

def parse(line) :
	return PasswordData(line)

#Problem code

def part1(data):
	counter = 0
	for entry in data:
		if entry.isValid():
			counter += 1
	return counter


def part2(data):
	counter = 0
	for entry in data:
		if entry.isValid2():
			counter += 1
	return counter

class PasswordData:

	def __init__(self, string):
		regex = re.compile(r'^(\d+)-(\d+) (\w+): (\w+)$')
		match = regex.match(string)
		self.min = int(match.group(1))
		self.max = int(match.group(2))
		self.char = match.group(3)
		self.password = match.group(4)

	def isValid(self):
		counter = 0
		for letter in self.password:
			if letter == self.char:
				counter += 1
		if (counter <= self.max and counter >= self.min):
			return True
		return False

	def isValid2(self):
		first = self.password[self.min-1]
		second = self.password[self.max-1]
		if (first == self.char or second == self.char) and first != second:
			return True
		return False

#Execution stuff

def test1():
	rawInput = "1-3 a: abcde\n1-3 b: cdefg\n2-9 c: ccccccccc"
	data = dataToParsedArray(rawInput)
	print(part1(data))
	return

def test2():
	rawInput = "1-3 a: abcde\n1-3 b: cdefg\n2-9 c: ccccccccc"
	data = dataToParsedArray(rawInput)
	print(part2(data))
	return

def main():
	rawInput = open("./input/2.txt").read()
	data = dataToParsedArray(rawInput)
	print(part1(data))
	print(part2(data))
	return

#test1()
#test2()
main()