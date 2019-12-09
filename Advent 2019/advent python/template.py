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

#test1()
#test2()
main()

#Python reminders
#range(start, end+1, step), len
#{}, for k in dict, for k,v in dict.items(), for v in dict.values()  
#set(), .add(x), .remove(x), .discard(x) no error if missing, x in s, |= union, &= intersect, -= difference, .copy()
#[], .append(), .insert(i,x), .pop([i]), .remove(x), .reverse(), sort(arr) in place, sorted(arr) new arr 
#map(single param function, list)
#filter(single param boolean returning function, list)
#reduce(2 param function, list)
#lambda x: x**2
#// integer division in python3
#sys.maxsize
#common global functions: abs() max() min() len()
#from queue import Queue ->thread safe, can be blocking, .put() .get()
#from threading import Thread ->thread = Thread(target = f). .start(), .join()
#from itertools import permutations -> permutations(list)
#from types import SimpleNamespace -> objet style = SimpleNamespace(**dict)	