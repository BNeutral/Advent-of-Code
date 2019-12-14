from collections import defaultdict
import math

#File parsing stuff
def dataToDict(stringData) :
	result = {}
	for line in stringData.split("\n"):
		line = line.strip()
		if line == "":
			continue
		formula = Formula(line)
		result[formula.outputName] = formula
	return result

#Problem code

def part1(data):
	tree = buildTree(data)
	return calculateOreNeeded(tree,1)

def part2(data):
	tree = buildTree(data)
	fuel = 1
	ore = calculateOreNeeded(tree, fuel)
	oneTrillion = 1000000000000
	window = 1
	wentOver = False
	repeats = set()
	while ore != oneTrillion:
		if not wentOver:
			if ore > oneTrillion:
				wentOver = True
			else:
				fuel += window
				window *= 2
		if wentOver:
			if ore <= oneTrillion and fuel in repeats:
				break
			if ore > oneTrillion:
				fuel -= window 
				window = max(window/2,1)
			else :
				fuel += window 
				window = max(window/2,1)	
			if window == 1:
				repeats.add(fuel)		
		ore = calculateOreNeeded(tree, fuel)
	return ore,fuel

def calculateOreNeeded(tree, fuelAmount):
	for node in tree.values():
		node.reset()
	tree["FUEL"].produce(fuelAmount)
	return tree["ORE"].produced

def buildTree(data):
	tree = {}
	for formula in data.values():
		name,amount = formula.outputName, formula.outputAmount
		tree[name] = TreeNode(name, amount)
	tree["ORE"] = TreeNode("ORE",1)
	for formula in data.values():
		name = formula.outputName
		for amount,inName in formula.inputs:
			tree[name].addChild(tree[inName],amount)
	return tree

class TreeNode:

	def __init__(self, name, produceAmount):
		self.name = name
		self.produceAmount = produceAmount
		self.children = []
		self.childrenCosts = []
		self.produced = 0
		self.leftOver = 0

	def addChild(self, node, cost):
		self.children.append(node)
		self.childrenCosts.append(cost)

	def produce(self, amount):
		needs = amount-self.leftOver
		self.leftOver = 0
		if needs < 0:
			self.leftOver = -needs
			return
		multiplier = math.ceil(needs/self.produceAmount)
		toProduce = self.produceAmount*multiplier
		self.produced += toProduce
		self.leftOver = toProduce - needs
		for x in range(len(self.children)):
			needs = self.childrenCosts[x]*multiplier
			self.children[x].produce(needs)

	def reset(self):
		self.produced = 0
		self.leftOver = 0

class Formula:

	def __init__(self, line):
		tmp = line.split("=>")
		inputs = tmp[0].split(",")
		output = self.inputToTuple(tmp[1])
		inputArray = []
		for inp in inputs:
			inputArray.append(self.inputToTuple(inp))
		self.inputs = inputArray
		self.outputAmount = output[0]
		self.outputName = output[1]

	def inputToTuple(self,string):
		string = string.strip()
		split = string.split(" ")
		return (int(split[0]),split[1].strip())

#Execution stuff

def test1():
	rawInput = "9 ORE => 2 A\n8 ORE => 3 B\n7 ORE => 5 C\n3 A, 4 B => 1 AB\n5 B, 7 C => 1 BC\n4 C, 1 A => 1 CA\n2 AB, 3 BC, 4 CA => 1 FUEL\n"
	data = dataToDict(rawInput)
	print(part1(data))
	rawInput = "157 ORE => 5 NZVS\n165 ORE => 6 DCFZ\n44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL\n12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ\n179 ORE => 7 PSHF\n177 ORE => 5 HKGWZ\n7 DCFZ, 7 PSHF => 2 XJWVT\n165 ORE => 2 GPVTF\n3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT\n"
	data = dataToDict(rawInput)
	print(part1(data))
	rawInput = "2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG\n17 NVRVD, 3 JNWZP => 8 VPVL\n53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL\n22 VJHF, 37 MNCFX => 5 FWMGM\n139 ORE => 4 NVRVD\n144 ORE => 7 JNWZP\n5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC\n5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV\n145 ORE => 6 MNCFX\n1 NVRVD => 8 CXFTF\n1 VJHF, 6 MNCFX => 4 RFSQX\n176 ORE => 6 VJHF\n"
	data = dataToDict(rawInput)
	print(part1(data))
	rawInput = "171 ORE => 8 CNZTR\n7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL\n114 ORE => 4 BHXH\n14 VRPVC => 6 BMBT\n6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL\n6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT\n15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW\n13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW\n5 BMBT => 4 WPTQ\n189 ORE => 9 KTJDG\n1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP\n12 VRPVC, 27 CNZTR => 2 XDBXC\n15 KTJDG, 12 BHXH => 5 XCVML\n3 BHXH, 2 VRPVC => 7 MZWV\n121 ORE => 7 VRPVC\n7 XCVML => 6 RJRHP\n5 BHXH, 4 VRPVC => 5 LTCX\n"
	data = dataToDict(rawInput)
	print(part1(data))
	return

def test2():
	rawInput = "157 ORE => 5 NZVS\n165 ORE => 6 DCFZ\n44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL\n12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ\n179 ORE => 7 PSHF\n177 ORE => 5 HKGWZ\n7 DCFZ, 7 PSHF => 2 XJWVT\n165 ORE => 2 GPVTF\n3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT\n"
	data = dataToDict(rawInput)
	print(part2(data))
	rawInput = "2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG\n17 NVRVD, 3 JNWZP => 8 VPVL\n53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL\n22 VJHF, 37 MNCFX => 5 FWMGM\n139 ORE => 4 NVRVD\n144 ORE => 7 JNWZP\n5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC\n5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV\n145 ORE => 6 MNCFX\n1 NVRVD => 8 CXFTF\n1 VJHF, 6 MNCFX => 4 RFSQX\n176 ORE => 6 VJHF\n"
	data = dataToDict(rawInput)
	print(part2(data))
	rawInput = "171 ORE => 8 CNZTR\n7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL\n114 ORE => 4 BHXH\n14 VRPVC => 6 BMBT\n6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL\n6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT\n15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW\n13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW\n5 BMBT => 4 WPTQ\n189 ORE => 9 KTJDG\n1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP\n12 VRPVC, 27 CNZTR => 2 XDBXC\n15 KTJDG, 12 BHXH => 5 XCVML\n3 BHXH, 2 VRPVC => 7 MZWV\n121 ORE => 7 VRPVC\n7 XCVML => 6 RJRHP\n5 BHXH, 4 VRPVC => 5 LTCX\n"
	data = dataToDict(rawInput)
	print(part2(data))
	return

def main():
	rawInput = open("./input/14.txt").read()
	data = dataToDict(rawInput)
	print(part1(data))
	print(part2(data))
	return

#test1()
#test2()
main()