from collections import defaultdict
from util import *
import time
from intcode import Interpreter

from threading import Lock

class NAT:

	def __init__(self, network):
		self.network = network
		self.x = None
		self.y = None
		self.lasty = None
		self.part1 = True
		self.part2 = True
		self.idleCounter = []
		self.lock = Lock()
		self.isReady = False

	def ready(self):
		for _ in range(len(self.network)):
			self.idleCounter.append(0)
		self.isReady = True

	def notifyIdle(self, id):
		self.idleCounter[id] = 1 #Supposedly this is thread safe
		if sum(self.idleCounter) == len(self.network):
			self.sendPacket()
			self.idleCounter[0] = 0 #Supposedly this is thread safe

	def notifyRunning(self, id):
		if not self.isReady:
			return
		self.idleCounter[id] = 0 #Supposedly this is thread safe

	def sendPacket(self):
		if self.y != None and self.x != None:
			if self.y == self.lasty and self.part2:
				print("Part 2 solution:", self.y)
				self.part2 = False
			self.network[0].giveInput( [self.x, self.y] )
			self.lasty = self.y

	def receivePacket(self, x, y):
		self.lock.acquire()
		if self.part1:
			print("Part 1 answer:", y)
			self.part1 = False
		self.x = x
		self.y = y 
		self.lock.release()

class NetWorker(Interpreter):

	def __init__(self, programArray, networkArray, nat, netId):
		super().__init__(programArray, defaultInput=-1) 
		self.network = networkArray
		self.id = netId
		self.nat = nat
		self.inputLock = Lock()
		self.giveInput( [netId] )		
		self.output = []		

	def _opOutput(self, pc, modes):
		self.output.append(self._read(pc+1,modes[0]))
		return pc+2

	#Sends the input to the interpreter
	def giveInput(self, values):
		self.inputLock.acquire()
		for value in values:
			self.inputs.put(value)
		self.awaitingInput = False
		self.inputLock.release()

	def getInput(self):
		self.inputLock.acquire()
		try:
			a = self.inputs.get(timeout=0.02) #Small timeout so all threads get time
			self.inputLock.release()
			self.nat.notifyRunning(self.id)
			return a
		except:
			self.inputLock.release()
			self.nat.notifyIdle(self.id)
			return self.defaultInput

	def runProgram(self):
		self.isRunning = True
		pc = 0
		while True:
			opcode,modes = super()._parseOpcodeAndModes(pc)
			newpc = self.ops[opcode](pc,modes)			
			if len(self.output) >= 3:
				target = self.output.pop(0)
				x = self.output.pop(0)
				y = self.output.pop(0)
				if target == 255:
					self.nat.receivePacket(x,y)
				if target > 0 and target < len(self.network):
					#print(target, x, y)
					program = self.network[target]
					program.giveInput([x,y])
			if newpc == -1:
				self.isRunning = False
				return
			pc = newpc

#Problem code

def part1and2(data, networkSize = 50):
	programs = []
	nat = NAT(programs)
	for x in range(networkSize):
		program = NetWorker(data, programs, nat, x)
		programs.append(program)
	print("Network setup")
	nat.ready()
	for x in range(networkSize):
		programs[x].runInThread()
	return "Network operational"

#Execution stuff

def main():
	print("Warning: There may be some data race somewhere, but I got lazy.")
	rawInput = open("./input/23.txt").read()
	data = commaSeparatedLineToInts(rawInput)
	print(part1and2(data))
	return

main()