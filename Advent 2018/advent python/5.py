import re
import string

#Problem code
def part1(data):
	return len(reactFast(data))

def part2(data):
	ascii = list(string.ascii_lowercase)
	minlen = len(data)
	for char in ascii:
		cleanedString = data.replace(char,"").replace(char.capitalize(),"")
		result = len(reactFast(cleanedString))
		if  result < minlen:
			minlen = result
	return minlen

def reactFast(data):
	result = ""
	for letter in data:
		if not result:
			result = result + letter
		elif letter == result[-1].swapcase():
			result = result[:-1]
		else:
			result = result + letter
	return result

#Execution stuff

def test1():
	data = "dabAcCaCBAcCcaDA"
	print(part1(data))
	return

def test2():
	data = "dabAcCaCBAcCcaDA"
	print(part2(data))
	return

def main():
	rawInput = open("./input/5.txt").read()
	data = rawInput.strip()
	print(part1(data))
	print(part2(data))
	return

main()
