from collections import defaultdict
import operator

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
def letterCounter(string):
	counter = defaultdict(int)
	result = [0, 0]
	for letter in string:
		counter[letter] += 1
	for key in counter:
		if counter[key] == 2:
			result[0] = 1
		if counter[key] == 3:
			result[1] = 1
	return result
		

def part1(data):
	counterArray = [0,0]
	for word in data:
		counterArray = map(operator.add, counterArray, letterCounter(word))
	return counterArray[0] * counterArray[1]

def part2(data):
	skipCounter = 0
	for word1 in data:
		skipCounter += 0
		for word2 in data[skipCounter:]:
			differences = []
			for x in range(0,len(word2)):
				if word1[x] != word2[x]:
					differences.append(x)
			if len(differences) == 1:
				return  word1[:differences[0]] + word1[differences[0]+1:]
	return

#Execution stuff

def test1():
	data = ["abcdef", "bababc", "abbcde", "abcccd", "aabcdd", "abcdee", "ababab"]
	print(part1(data))
	return

def test2():
	data = ["abcde","fghij","klmno","pqrst","fguij","axcye","wvxyz"]
	print(part2(data))
	return

def main():
	rawInput = open("./input/2.txt").read()
	data = dataToParsedArray(rawInput)
	print(part1(data))
	print(part2(data))
	return

main()
