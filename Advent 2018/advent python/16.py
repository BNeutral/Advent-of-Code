import copy

#File parsing stuff
def dataToParsedArray(stringData) :
	samples = []
	instructions = [] 
	lines = stringData.split("\n")
	x = 0
	while x < len(lines) :
		line = lines[x].strip()
		if line != "":
			if line[0] == 'B':
				samples.append(Sample(line,lines[x+1].strip(),lines[x+2].strip()))
				x += 2
			else:
				instructions.append(map(int, line.split(" ")))
		x += 1
	return samples, instructions

#Problem code
def part1(samples):
	cpu = CPU()
	sampleCounter = 0
	for sample in samples:
		if cpu.behavesLike(sample) >= 3:
			sampleCounter += 1
	return sampleCounter

def part2(samples, instructions):
	cpu = CPU()
	cpu.decipher(samples)
	cpu.setRegisters([0,0,0,0])
	for instruction in instructions:
		cpu.runInstruction(instruction)	
	return cpu.registers[0]

class Sample:

	def __init__(self, line1, line2, line3):
		self.before = map(int, line1[9:-1].split(","))
		self.instruction = map(int, line2.split(" "))
		self.after = map(int, line3[9:-1].split(","))

	def __repr__(self):
		return str(self.__dict__)

class CPU:

	def __init__(self):
		self.registers = [0,0,0,0]
		self.decipheredFunctions = [None] * len(CPU.functions)
		
	#Returns how many functions the sample behaves like
	def behavesLike(self, sample):
		counter = 0
		for function in CPU.functions:
			self.setRegisters(sample.before)
			self.runMysteryInstruction(function, sample.instruction[1:])
			if self.registers == sample.after:
				counter += 1
		return counter

	#Deduces the functions from the samples
	def decipher(self,samples):
		functionLookup = [set() for _ in range(len(CPU.functions))]
		for sample in samples:
			sampleMatches = set()
			for x in range(len(CPU.functions)):
				self.setRegisters(sample.before)
				self.runMysteryInstruction(CPU.functions[x], sample.instruction[1:])
				if self.registers == sample.after: #If it matches, put the CPU.functions idx on a set
					sampleMatches.add(x)
			id = sample.instruction[0]
			if len(functionLookup[id]) == 0: #If empty, add first guess
				functionLookup[id] = sampleMatches
			else: #Intersect guesses
				functionLookup[id] = functionLookup[id] & sampleMatches
			if len(functionLookup[id]) == 1: #Down to one, remove from others
				for x in range(len(functionLookup)):
					if x != id:
						functionLookup[x] = functionLookup[x] - functionLookup[id]
		for x in range(len(functionLookup)): #Set the proper functions in the object list
			self.decipheredFunctions[x] = CPU.functions[functionLookup[x].pop()]

	#Runs an instruction provided, expects an array of 3 registers/immediates
	def runMysteryInstruction(self, function, data):
		return function(self, data[0], data[1], data[2])
	
	#Runs an instruction that comes as a 4 length member array
	def runInstruction(self, data):
		return self.decipheredFunctions[data[0]](self, data[1], data[2], data[3])

	#Sets the registers to the values provided in the array of length 4
	def setRegisters(self,array):
		self.registers = copy.deepcopy(array)

	def addr(self,ra,rb,rc):
		self.registers[rc] = self.registers[ra]+self.registers[rb]

	def addi(self,ra,ib,rc):
		self.registers[rc] = self.registers[ra]+ib

	def mulr(self,ra,rb,rc):
		self.registers[rc] = self.registers[ra]*self.registers[rb]

	def muli(self,ra,ib,rc):
		self.registers[rc] = self.registers[ra]*ib

	def banr(self,ra,rb,rc):
		self.registers[rc] = self.registers[ra]&self.registers[rb]

	def bani(self,ra,ib,rc):
		self.registers[rc] = self.registers[ra]&ib

	def borr(self,ra,rb,rc):
		self.registers[rc] = self.registers[ra]|self.registers[rb]

	def bori(self,ra,ib,rc):
		self.registers[rc] = self.registers[ra]|ib

	def setr(self,ra,b,rc):
		self.registers[rc] = self.registers[ra]

	def seti(self,ia,b,rc):
		self.registers[rc] = ia

	def gtir(self,ia,rb,rc):
		if ia > self.registers[rb]:
			self.registers[rc] = 1
		else:
			self.registers[rc] = 0

	def gtri(self,ra,ib,rc):
		if self.registers[ra] > ib:
			self.registers[rc] = 1
		else:
			self.registers[rc] = 0

	def gtrr(self,ra,rb,rc):
		if self.registers[ra] > self.registers[rb]:
			self.registers[rc] = 1
		else:
			self.registers[rc] = 0

	def eqir(self,ia,rb,rc):
		if ia == self.registers[rb]:
			self.registers[rc] = 1
		else:
			self.registers[rc] = 0

	def eqri(self,ra,ib,rc):
		if self.registers[ra] == ib:
			self.registers[rc] = 1
		else:
			self.registers[rc] = 0

	def eqrr(self,ra,rb,rc):
		if self.registers[ra] == self.registers[rb]:
			self.registers[rc] = 1
		else:
			self.registers[rc] = 0

	def __repr__(self):
		return str(self.__dict__)

	functions = [addr,addi,mulr,muli,banr,bani,bori,borr,eqir,eqri,eqrr,gtir,gtri,gtrr,seti,setr]

#Execution stuff

def test1():
	rawInput = "Before: [3, 2, 1, 1]\n9 2 1 2\nAfter:  [3, 2, 2, 1]"
	samples, _ = dataToParsedArray(rawInput)
	cpu = CPU()
	print(cpu.behavesLike(samples[0]))
	return

def main():
	rawInput = open("./input/16.txt").read()
	samples, instructions = dataToParsedArray(rawInput)
	print(part1(samples))
	print(part2(samples, instructions))
	return

#test1()
main()
