import sys
import re

#File parsing stuff
def dataToParsedArray(stringData) :
	lines = stringData.split("\n")
	initialRegex = re.compile(r'initial state: (.*)$')
	baseString = initialRegex.match(lines[0].strip()).groups(0)[0]
	rules = {}
	for line in lines[1:]:
		line = line.strip()
		if line != "":
			rule = Rule(line)
			rules[tuple(rule.arrayPattern)] = rule.result
	plants = stringToPlantArray(baseString)
	return plants, rules

#Problem code

def solve(plants, rules, generations):
	leftCounter = 0
	x = 0
	prevSum = 0
	while x < generations:
		x+= 1
		plants, leftCounter = expandIfNeeded(plants, leftCounter)
		newPlants = [0 for _ in range(len(plants))]
		for start in range(len(plants)-4):
			plantSlice = tuple(plants[start:start+5])
			if plantSlice in rules:
				newPlants[start+2] = rules[tuple(plantSlice)]
		plants = newPlants
		sumP = 0
		for i in range(len(plants)):
			if plants[i] == 1:
				sumP += i + leftCounter
		delta = sumP-prevSum
		if x > 120: #Seems it stabilizes around here. Todo: Better check
			return sumP+(generations-x)*delta
		prevSum = sumP
	return sumP

def printPlants(plants):
	for x in plants:
		if x == 1:
			sys.stdout.write('#')
		else:
			sys.stdout.write('.')
	sys.stdout.flush()

def expandIfNeeded(array, leftCounter):
	newArray = list(array)
	if sum(array[:6]) == 0: #Reduce left
		newArray = newArray[3:]
		leftCounter += 3
	elif sum(array[:3]) > 0: #Pad left
		newArray = [0,0,0] + newArray
		leftCounter -= 3
	if sum(array[-3:]) > 0: #Pad right
		newArray = newArray + [0,0,0]
	return newArray, leftCounter
	
def stringToPlantArray(string):
	result = []
	for letter in string:
		result.append(characterToPlant(letter))
	return result

def characterToPlant(letter):
	if letter == '#':
		return 1
	elif letter == '.':
		return 0

class Rule:

	def __init__(self, string):
		regex = re.compile(r'^([.#]+) => ([.#])$')
		matches = regex.match(string)
		self.arrayPattern = stringToPlantArray(matches.groups(0)[0])
		self.result = characterToPlant(matches.groups(0)[1])

	def __repr__(self):
		return str(self.arrayPattern)+"=>"+str(self.result)

#Execution stuff

def test1():
	string = "initial state: #..#.#..##......###...###\n\n...## => #\n..#.. => #\n.#... => #\n.#.#. => #\n.#.## => #\n.##.. => #\n.#### => #\n#.#.# => #\n#.### => #\n##.#. => #\n##.## => #\n###.. => #\n###.# => #\n####. => #"
	state,rules = dataToParsedArray(string)
	print(solve(state, rules, 20))
	return

def main():
	rawInput = open("./input/12.txt").read()
	state,rules = dataToParsedArray(rawInput)
	print(solve(state, rules, 20))
	print(solve(state, rules, 50000000000))
	return

main()
