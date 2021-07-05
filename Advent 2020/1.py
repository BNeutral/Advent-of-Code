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
	return int(line)

#Problem code

def part1(data):
	for x in range(len(data)):
		for y in range(x+1,len(data)):
			n1 = data[x]
			n2 = data[y]
			if ((n1+n2) == 2020):
				return n1*n2
	return

def part2(data):
	for x in range(len(data)):
		for y in range(x+1,len(data)):
			for z in range(x+2,len(data)):
				n1 = data[x]
				n2 = data[y]
				n3 = data[z]
				if ((n1+n2+n3) == 2020):
					return n1*n2*n3
	return

#Execution stuff

def test1():
	rawInput = "1721\n979\n366\n299\n675\n1456"
	data = dataToParsedArray(rawInput)
	print(part1(data))
	return

def test2():
	rawInput = "1721\n979\n366\n299\n675\n1456"
	data = dataToParsedArray(rawInput)
	print(part2(data))
	return

def main():
	rawInput = open("./input/1.txt").read()
	data = dataToParsedArray(rawInput)
	print(part1(data))
	print(part2(data))
	return

#test1()
#test2()
main()