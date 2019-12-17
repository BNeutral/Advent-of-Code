from util import *

#Problem code

def part1(data, iterations):
	return fft(data,iterations)[0:8]

def part2(data):
	offset = getOffset(data)
	longData = data.copy()*10000
	result = upperHalffft(longData,100,offset)
	return result[offset:offset+8]

def getOffset(data):
	offset = 0
	for x in range(7):
			offset += data[x] * (10**(6-x))
	return offset

def upperHalffft(data, iterations, offset):
	length = len(data)
	if offset < length//2:
		return "Can't compute"
	newData = [0] * length
	for _ in range(iterations):
		newData[length-1] = data[length-1]
		for i in range(length-2,offset-1,-1):
			dataElement = data[i]
			result = dataElement + newData[i+1]
			newData[i] = result%10
		data = newData
		newData = [0] * len(data)
	return data

def fft(data, iterations):
	newData = [0] * len(data)
	for _ in range(iterations):
		for i in range(len(data)):
			sumResult = 0
			for j in range(i,len(data)):
				dataElement = data[j]
				patternElement = getPatternDigit(i+1,j+1)
				result = dataElement*patternElement
				sumResult += result
			newData[i] = abs(sumResult)%10
		data = newData
		newData = [0] * len(data)
	return data
		
basePattern = [0,1,0,-1]
def getPatternDigit(multiplier, i):
	patternLength = 4*multiplier
	return basePattern[i % patternLength // multiplier]

#Execution stuff

def test1():
	rawInput = "12345678"
	data = lineDigitsToArray(rawInput)
	print(part1(data,4))
	rawInput = "80871224585914546619083218645595"
	data = lineDigitsToArray(rawInput)
	print(part1(data,100))
	rawInput = "19617804207202209144916044189917"
	data = lineDigitsToArray(rawInput)
	print(part1(data,100))
	rawInput = "69317163492948606335995924319873"
	data = lineDigitsToArray(rawInput)
	print(part1(data,100))
	return

def test2():
	rawInput = "03036732577212944063491565474664"
	data = lineDigitsToArray(rawInput)
	print(part2(data))
	rawInput = "02935109699940807407585447034323"
	data = lineDigitsToArray(rawInput)
	print(part2(data))
	return

def test3():
	res = []
	for x in range(10):
		res.append([])
		for i in range(20):
			res[x].append(getPatternDigit(x+1,i))
	for array in res:
		print(array)

def main():
	rawInput = open("./input/16.txt").read()
	data = lineDigitsToArray(rawInput)
	print(part1(data,100))
	print(part2(data))
	return

#test1()
#test2()
#test3()
main()