from queue import Queue

class Interpreter:

	#array is an array of ints contains the program 
	#inp is the input as an array
	def __init__(self, array, inp, useDefaultInput=True):
		self.array = array.copy()
		self.inputs = Queue()
		for i in inp:
			self.inputs.put(i)
		self.defaultInput = array[-1]
		self.useDefaultInput = useDefaultInput
		self.output = Queue()
		self.relativeBase = 0
		self.isRunning = False
		self.awaitingInput = False

	def __repr__(self):
		return str(self.__dict__)

	def runProgram(self):
		self.isRunning = True
		ops = {
			1:self.opAdd,
			2:self.opMul,
			3:self.opInput,
			4:self.opOutput,
			5:self.opJmpTrue,
			6:self.opJmpFalse,
			7:self.opLessThan,
			8:self.opEquals,
			9:self.opAdjustBase,
			99:self.opHalt
		}
		pc = 0
		while True:
			opcode,modes = self.parseOpcodeAndModes(pc)
			newpc = ops[opcode](pc,modes)
			if newpc == -1:
				self.isRunning = False
				return
			pc = newpc

	def getInput(self):
		if self.useDefaultInput:
			try:
				a = self.inputs.get(False)
				return a
			except:
				return self.defaultInput
		else:
			self.awaitingInput = True
			inp = self.inputs.get()
			return inp

	def giveInput(self, value):
		self.inputs.put(value)
		self.awaitingInput = False

	def opAdd(self, pc, modes):
		self.write(pc+3, modes[2], self.read(pc+1,modes[0]) + self.read(pc+2,modes[1]))
		return pc+4

	def opMul(self, pc, modes):
		self.write(pc+3, modes[2], self.read(pc+1,modes[0]) * self.read(pc+2,modes[1]))
		return pc+4

	def opInput(self, pc, modes):
		self.write(pc+1, modes[0], self.getInput())
		return pc+2

	def opOutput(self, pc, modes):
		self.output.put(self.read(pc+1,modes[0]))
		return pc+2

	def opJmpTrue(self, pc, modes):
		if self.read(pc+1, modes[0]) != 0:
			return self.read(pc+2, modes[1])
		return pc+3

	def opJmpFalse(self, pc, modes):
		if self.read(pc+1, modes[0]) == 0:
			return self.read(pc+2, modes[1])
		return pc+3

	def opLessThan(self, pc, modes):
		if self.read(pc+1,modes[0]) < self.read(pc+2,modes[1]):
			self.write(pc+3, modes[2],1)
		else:
			self.write(pc+3, modes[2],0)
		return pc+4

	def opEquals(self, pc, modes):
		if self.read(pc+1,modes[0]) == self.read(pc+2,modes[1]):
			self.write(pc+3, modes[2],1)
		else:
			self.write(pc+3, modes[2],0)
		return pc+4

	def opHalt(self, pc, modes):
		return -1

	def opAdjustBase(self, pc, modes):
		self.relativeBase += self.read(pc+1,modes[0])
		return pc+2

	def parseOpcodeAndModes(self,pc):
		instruction = self.array[pc]
		opcode = instruction % 100
		modes = [0,0,0]
		for x in range(len(modes)):
			modes[x] = (instruction//pow(10,2+x)) % 10
		return opcode,modes

	def checkSize(self,index,mode):
		self.makeIndexValid(index)
		if mode == 0:
			self.makeIndexValid(self.array[index])
		elif mode == 2:
			self.makeIndexValid(self.array[index]+self.relativeBase)

	def makeIndexValid(self,index):
		size = len(self.array)
		if index >= size:
			dif = index - len(self.array) + 1
			self.array.extend([0]*dif)

	def read(self, index, mode):
		self.checkSize(index,mode)
		if mode == 0:
			return self.array[self.array[index]]
		elif mode == 1:
			return self.array[index]
		elif mode == 2:
			return self.array[self.array[index]+self.relativeBase]

	def write(self, index, mode, value):
		self.checkSize(index,mode)
		if mode == 0:
			self.array[self.array[index]] = value
		elif mode == 1:
			self.array[index] = value
		elif mode == 2:
			self.array[self.array[index]+self.relativeBase] = value	