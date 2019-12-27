from queue import Queue
from threading import Thread

class Interpreter:

	#programArray is an array of ints contains the program 
	#inp is the starting input as an array
	#defaultInput is the input the program should return when fetching input as a default
	def __init__(self, programArray, inp=[], defaultInput=None):
		self.array = programArray.copy()
		self.inputs = Queue()
		for i in inp:
			self.inputs.put(i)
		self.defaultInput = defaultInput
		self.output = Queue()
		self.relativeBase = 0
		self.isRunning = False
		self.awaitingInput = False
		self.ops = {
			1:self._opAdd,
			2:self._opMul,
			3:self._opInput,
			4:self._opOutput,
			5:self._opJmpTrue,
			6:self._opJmpFalse,
			7:self._opLessThan,
			8:self._opEquals,
			9:self._opAdjustBase,
			99:self._opHalt
		}

	def __repr__(self):
		return str(self.__dict__)

	def runInThread(self):
		thread = Thread(target = self.runProgram)
		thread.start()
		return thread

	def runProgram(self):
		self.isRunning = True
		pc = 0
		while True:
			opcode,modes = self._parseOpcodeAndModes(pc)
			newpc = self.ops[opcode](pc,modes)
			if newpc == -1:
				self.isRunning = False
				return
			pc = newpc

	#Turns a string into input for the program
	def sendASCIIInput(self, input):
		for char in input:
			self.inputs.put(ord(char))
		self.inputs.put(10)

	#Returns a string with the output, blocks if size is known, has a timeout otherwise
	def getASCIIOutput(self, size=0, timeout=5):
		result = ""
		try:
			if size != 0:
				for _ in range(size):
					result += str(chr((self.output.get())))
			else:
				while True:
					result += str(chr((self.output.get(timeout=timeout))))
		except:
			pass
		return result

	#Gets the input 
	def getInput(self):
		if self.defaultInput:
			try:
				a = self.inputs.get(False)
				return a
			except:
				return self.defaultInput
		else:
			self.awaitingInput = True
			inp = self.inputs.get()
			return inp

	#Sends the input to the interpreter
	def giveInput(self, value):
		self.inputs.put(value)
		self.awaitingInput = False

	def _opAdd(self, pc, modes):
		self._write(pc+3, modes[2], self._read(pc+1,modes[0]) + self._read(pc+2,modes[1]))
		return pc+4

	def _opMul(self, pc, modes):
		self._write(pc+3, modes[2], self._read(pc+1,modes[0]) * self._read(pc+2,modes[1]))
		return pc+4

	def _opInput(self, pc, modes):
		self._write(pc+1, modes[0], self.getInput())
		return pc+2

	def _opOutput(self, pc, modes):
		self.output.put(self._read(pc+1,modes[0]))
		return pc+2

	def _opJmpTrue(self, pc, modes):
		if self._read(pc+1, modes[0]) != 0:
			return self._read(pc+2, modes[1])
		return pc+3

	def _opJmpFalse(self, pc, modes):
		if self._read(pc+1, modes[0]) == 0:
			return self._read(pc+2, modes[1])
		return pc+3

	def _opLessThan(self, pc, modes):
		if self._read(pc+1,modes[0]) < self._read(pc+2,modes[1]):
			self._write(pc+3, modes[2],1)
		else:
			self._write(pc+3, modes[2],0)
		return pc+4

	def _opEquals(self, pc, modes):
		if self._read(pc+1,modes[0]) == self._read(pc+2,modes[1]):
			self._write(pc+3, modes[2],1)
		else:
			self._write(pc+3, modes[2],0)
		return pc+4

	def _opHalt(self, pc, modes):
		return -1

	def _opAdjustBase(self, pc, modes):
		self.relativeBase += self._read(pc+1,modes[0])
		return pc+2

	def _parseOpcodeAndModes(self,pc):
		instruction = self.array[pc]
		opcode = instruction % 100
		modes = [0,0,0]
		for x in range(len(modes)):
			modes[x] = (instruction//pow(10,2+x)) % 10
		return opcode,modes

	def _checkSize(self,index,mode):
		self._makeIndexValid(index)
		if mode == 0:
			self._makeIndexValid(self.array[index])
		elif mode == 2:
			self._makeIndexValid(self.array[index]+self.relativeBase)

	def _makeIndexValid(self,index):
		size = len(self.array)
		if index >= size:
			dif = index - len(self.array) + 1
			self.array.extend([0]*dif)

	def _read(self, index, mode):
		self._checkSize(index,mode)
		if mode == 0:
			return self.array[self.array[index]]
		elif mode == 1:
			return self.array[index]
		elif mode == 2:
			return self.array[self.array[index]+self.relativeBase]

	def _write(self, index, mode, value):
		self._checkSize(index,mode)
		if mode == 0:
			self.array[self.array[index]] = value
		elif mode == 1:
			self.array[index] = value
		elif mode == 2:
			self.array[self.array[index]+self.relativeBase] = value	