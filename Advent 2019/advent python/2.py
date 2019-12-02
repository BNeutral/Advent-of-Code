from collections import defaultdict
import re

#File parsing stuff
def dataToParsedArray(stringData) :
	result = [] 
	for line in stringData.split(","):
		line = line.strip()
		if line != "":
			result.append(parse(line))
	return result

def parse(line) :
	return int(line)

#Problem code

def part1(data):
	data[1] = 12
	data[2] = 2
	return runProgram(data)

def runProgram(array, i=0):
	if array[i] == 1:
		array[array[i+3]] = array[array[i+1]]+array[array[i+2]]
	elif array[i] == 2:
		array[array[i+3]] = array[array[i+1]]*array[array[i+2]]
	elif array[i] == 99:
		return array[0]
	return runProgram(array,i+4)

def part2(data, target):
	for x in range(0,100):
		for y in range(0,100):
			newData = data.copy()
			newData[1] = x
			newData[2] = y
			if runProgram(newData) == target:
				return x,y

#Execution stuff

def test1():
	rawInput = "1,9,10,3,2,3,11,0,99,30,40,50"
	data = dataToParsedArray(rawInput)
	res = runProgram(data)
	print(res)
	return

def main():
	rawInput = open("./input/2.txt").read()
	data = dataToParsedArray(rawInput)
	#print(part1(data))
	print(part2(data, 19690720))
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