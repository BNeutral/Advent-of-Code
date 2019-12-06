from collections import defaultdict
import re

#Problem code

def isValid(number):
	hasDouble = False
	num = str(number)
	for x in range(1,len(num)):
		if int(num[x]) < int(num[x-1]):
			return False
		if num[x] == num[x-1]:
			hasDouble = True
	return hasDouble

def isValid2(number):
	doubleGroups = set()
	num = str(number)
	for x in range(1,len(num)):
		if int(num[x]) < int(num[x-1]):
			return False
		if num[x] == num[x-1]:
			doubleGroups.add(num[x])
			if x >= 2:
				if num[x] == num[x-2]:
					doubleGroups.remove(num[x])
	return len(doubleGroups) > 0

def checkRangeValid(start,end,function):
	valids = 0
	for x in range(start,end+1):
		if function(x):
			valid += 1
	return valids

def part1(start,end):
	return checkRangeValid(start,end,isValid)

def part2(start,end):
	return checkRangeValid(start,end,isValid2)

#Execution stuff

def test1():
	print(isValid(111111))
	print(isValid(223450))
	print(isValid(123789))
	print(isValid(110111))
	print(isValid(223457))
	print(isValid(123788))
	return

def test2():
	print(isValid2(112233))
	print(isValid2(123444))
	print(isValid2(111122))
	return

def main():
	print(part1(108457,562041))
	print(part2(108457,562041))
	return

#test1()
#test2()
main()