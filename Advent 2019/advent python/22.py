from collections import defaultdict
from util import *
import re

#File parsing stuff
def dataToParsedArray(stringData) :
	result = [] 
	for line in stringData.split("\n"):
		line = line.strip()
		result.append(line)
	return result

#Problem code

def part1(data, deckSize=10007, targetCard=0):
	deck = []
	for x in range(deckSize):
		deck.append(x)
	for line in data:
		split = line.split(" ")
		if split[-1] == "stack":
			deck = toNewStack(deck)
		else:
			n = int(split[-1])
			op = split[-2]
			if op == "increment":
				deck = dealIncrement(deck,n)
			elif op == "cut":
				deck = cutN(deck,n)
			else:
				print("Unknown operation")
	return deck, deck.index(targetCard)

def toNewStack(array):
	return array[::-1]

def cutN(array, n):
	return array[n:]+array[:n]

def dealIncrement(array, n):
	newDeck = array.copy()
	for x in range(len(array)):
		newDeck[ (x*n) % len(array) ] = array[x]
	return newDeck

#Composition of linear functions is another linear function
#If the function is linear, f(x) = ax+b
# Then repeating the opreation, f(f(x)) = a(ax+b)+b = a^2 x + ab + b = a^2 x + (a+1)b 
# f(f(x)) = a(ax+b)+b = a^2 x + ab + b = a^2 x + (a+1)b 
# And eventually applying it n times a^n x + (a^(n-1) + a^(n-2) + ... + 1) b = a^n x + (a^n) / (a-1) b
# Note: a^0 + a + a^2 + a^3 + ... + a^n = geometric series = (a^n+1 - 1) / (a-1)
def part2(data, deckSize=119315717514047, shuffles=101741582076661, targetPosition=2020):
	functions = toInverseTupleInstructions(data)
	Fx = applyReversedInput(functions)
	Gx = applyReversedInput(functions, deckSize, Fx)
	A = (Fx-Gx) * modinv(targetPosition-Fx+deckSize, deckSize) % deckSize
	B = (Fx-A*targetPosition) % deckSize
	return (pow(A, shuffles, deckSize)*targetPosition + (pow(A, shuffles, deckSize)-1) * modinv(A-1, deckSize) * B) % deckSize

def applyReversedInput(functions, deckSize=119315717514047, targetPosition=2020):
	currentPos = targetPosition
	for tup in functions:
		currentPos = tup[0](deckSize, tup[1], currentPos)
	return currentPos

def toInverseTupleInstructions(data):
	singleParse = []
	for line in data[::-1]:
		split = line.split(" ")
		if split[-1] == "stack":
			singleParse.append( (fromNewStack,0) )
		else:
			n = int(split[-1])
			op = split[-2]
			if op == "increment":
				singleParse.append( (fromIncrement,n) )
			elif op == "cut":
				singleParse.append( (fromCutN,n) )
			else:
				print("Unknown operation")
	return singleParse

# Returns what the card post would have been before a newstack shuffle
def fromNewStack(arrayLen, n, pos):
	return arrayLen-1-pos

# Returns what the card post would have been before a cut shuffle
def fromCutN(arrayLen, n, pos):
	return (pos+n)%arrayLen

def fromIncrement(arrayLen, n, pos):
	mod = modinv(n, arrayLen) #n * mod % arrayLen = 1
	return (mod * pos) % arrayLen 

#Execution stuff

def test1():
	cards = [0,1,2,3,4,5,6,7,8,9]
	print("Stack:",toNewStack(cards))
	print("Cut 3:",cutN(cards,3))
	print("Cute -4:",cutN(cards,-4))
	print("Increment 3:",dealIncrement(cards,3))
	print("--------")
	rawInput = "deal with increment 7\ndeal into new stack\ndeal into new stack"
	data = dataToParsedArray(rawInput)
	print(part1(data, 10))
	rawInput = "cut 6\ndeal with increment 7\ndeal into new stack"
	data = dataToParsedArray(rawInput)
	print(part1(data, 10))
	rawInput = "deal with increment 7\ndeal with increment 9\ncut -2"
	data = dataToParsedArray(rawInput)
	print(part1(data, 10))
	return

def test2():
	print("-- Stack")
	print(fromNewStack(10,0,9) == 0)
	print(fromNewStack(10,0,8) == 1)
	print("-- Cut")
	print(fromCutN(10,3,0) == 3)
	print(fromCutN(10,3,7) == 0)
	print(fromCutN(10,-4,0) == 6)
	print(fromCutN(10,-4,4) == 0)
	print("-- Increm")
	print(fromIncrement(10,3,0) == 0)
	print(fromIncrement(10,3,1) == 7)
	print(fromIncrement(10,3,2) == 4)
	print(fromIncrement(10,3,3) == 1)
	print(fromIncrement(10,3,4) == 8)
	print(fromIncrement(10,3,5) == 5)
	print(fromIncrement(10,3,6) == 2)
	print(fromIncrement(10,3,7) == 9)
	print(fromIncrement(10,3,8) == 6)
	print(fromIncrement(10,3,9) == 3)
	print("--------")
	rawInput = open("./input/22.txt").read()
	data = dataToParsedArray(rawInput)
	functions = toInverseTupleInstructions(data)
	print(applyReversedInput(functions, 10007, 2939) == 2019)
	return

def main():
	rawInput = open("./input/22.txt").read()
	data = dataToParsedArray(rawInput)
	_,result1 = part1(data, 10007, 2019)
	print(result1)
	print(part2(data))
	return

#test1()
#test2()
main()