from queue import Queue
from threading import Thread
from itertools import permutations
from types import SimpleNamespace
from intcode import Interpreter
from util import *

def part1(data):
	maxOutput = 0
	toPermutate = [0,1,2,3,4]
	for phases in permutations(toPermutate) :
		maxOutput = max(runWithPhases(data,phases),maxOutput)
	return maxOutput

def part2(data):
	maxOutput = 0
	toPermutate = [5,6,7,8,9]
	for phases in permutations(toPermutate) :
		maxOutput = max(runFeedback(data,phases),maxOutput)
	return maxOutput

def runWithPhases(data, phases):
	startQueue = Queue()
	startQueue.put(0)
	fakeAmp = {"output":startQueue}
	amps = [SimpleNamespace(**fakeAmp)]	
	for x in range(len(phases)):
		t = Interpreter(data,[phases[x],amps[x].output.get()])
		t.runProgram()
		amps.append(t)
	return amps[-1].output.get()

def runFeedback(data, phases):
	amps = []
	threads = []
	for x in range(len(phases)):
		startingInput = [phases[x]]
		if x == 0:
			startingInput.append(0)
		amps.append(Interpreter(data,startingInput,False))
	for x in range(len(amps)):
		amps[x].output = amps[(x+1)%len(amps)].inputs
	for amp in amps:
		thread = Thread(target = amp.runProgram)
		thread.start()
		threads.append(thread)
	for thread in threads:
		thread.join()
	return amps[-1].output.get()

#Execution stuff

def test1():
	test1_1()
	test1_2()
	test1_3()

def test1_1():
	rawInput = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"
	data = commaSeparatedLineToInts(rawInput)
	print(runWithPhases(data, [4,3,2,1,0]))
	return

def test1_2():
	rawInput = "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"
	data = commaSeparatedLineToInts(rawInput)
	print(runWithPhases(data, [0,1,2,3,4]))
	return

def test1_3():
	rawInput = "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"
	data = commaSeparatedLineToInts(rawInput)
	print(runWithPhases(data, [1,0,4,3,2]))
	return

def test2():
	rawInput = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"
	data = commaSeparatedLineToInts(rawInput)
	print(runFeedback(data, [9,8,7,6,5]))
	return

def main():
	rawInput = open("./input/7.txt").read()
	data = commaSeparatedLineToInts(rawInput)
	print(part1(data))
	print(part2(data))
	return

#test1()
#test2()
main()
	