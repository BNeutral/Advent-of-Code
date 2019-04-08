#File parsing stuff
def dataToParsedArray(stringData) :
	instructions = [] 
	lines = stringData.split("\n")
	x = 0
	while x < len(lines) :
		line = lines[x].strip()
		if line != "":
				instructions.append(parse(line))
		x += 1
	return instructions

def parse(line) :
	split = line.split(" ")
	instruction = [split[0]]
	if len(split) > 1:
		instruction.extend(map(int, split[1:]))
	return instruction

#Problem code
def part1(instructions):
	cpu = CPU()
	cpu.run(instructions)
	return cpu.registers[0]

def part2(value):
	pairs = set()
	for i in range(1, int(value**0.5)+1):
		if value % i == 0:			
			pairs.add(i)
			pairs.add(value / i)
	return sum(pairs)

def part2Print(instructions):
	cpu = CPU()
	#instructions[1-1][0] = "nop"
	#instructions[2-1][0] = "nop"
	cpu.registers[0] = 1
	#cpu.registers[1] = 10551280
	#cpu.registers[5] = 10551280
	cpu.run(instructions)
	return cpu.registers[0]

class CPU:

	def __init__(self):
		self.registers = [0,0,0,0,0,0]
		self.ip = 0
		self.ipIndex = None

	#Runs an instruction that comes as a 4 length member array
	def run(self, instructions):
		self.ipIndex = instructions.pop(0)[1]
		while self.ip < len(instructions):
			self.runInstruction(instructions[self.ip])
	
	def runInstruction(self, instruction):
		print "Instruction start"
		print self.ip, self.registers
		print instruction
		self.registers[self.ipIndex] = self.ip
		CPU.functions[instruction[0]](self,instruction[1],instruction[2],instruction[3])
		self.ip = self.registers[self.ipIndex]
		self.ip += 1
		print self.ip, self.registers
		print "Instruction end"

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

	def nop(self,a,b,c):
		return

	def __repr__(self):
		return str(self.__dict__)

	functions = {"nop":nop, "addr" : addr, "addi" : addi, "mulr" : mulr, "muli" : muli, "banr" : banr, "bani": bani, "bori":bori, "borr": borr, "eqir": eqir, "eqri" : eqri, "eqrr" : eqrr, "gtir" : gtir, "gtri" : gtri, "gtrr" : gtrr, "seti" : seti, "setr" : setr}

#Execution stuff

def test1():
	rawInput = "#ip 0\nseti 5 0 1\nseti 6 0 2\naddi 0 1 0\naddr 1 2 3\nsetr 1 0 0\nseti 8 0 4\nseti 9 0 5"
	instructions = dataToParsedArray(rawInput)
	cpu = CPU()
	cpu.run(instructions)
	print(cpu.registers[0])
	return

def main():
	rawInput = open("./input/19.txt", "r").read()
	instructions = dataToParsedArray(rawInput)
	print(part2(10551282))
	return

#test1()
main()
