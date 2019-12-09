from collections import defaultdict
import re
import sys

#Problem code
def part1(data):
	return Image(data,25,6).corruptionCheck()

def part2(data):
	image = Image(data,25,6)
	image.merge()
	return str(image)

class Image:

	def __init__(self, stringData, width, height):
		self.data = list(map(int,stringData))
		self.width = width
		self.height = height
		self.pixelCount = width*height
		self.layers = []
		self._toLayers()
		self.mergedImage = self.layers[-1]

	def _toLayers(self):
		for x in range(len(self.data)//self.pixelCount):
			start = x*self.pixelCount
			end = start+self.pixelCount
			self.layers.append(self.data[start:end])

	def corruptionCheck(self):
		minZeroCount = sys.maxsize
		bestArray = None
		for array in self.layers:
			zeros = array.count(0)
			if zeros < minZeroCount:
				minZeroCount = zeros
				bestArray = array
		return bestArray.count(1) * bestArray.count(2)

	def merge(self):
		for layer in reversed(self.layers):
			for x in range(len(layer)):
				pixel = layer[x]
				if pixel != 2:
					self.mergedImage[x] = pixel

	def layerToStr(self,layer):
		printchars = ["░", "▓", " "]
		result = ""
		for row in range(self.height):
			for x in range(self.width):
				result += printchars[layer[row*self.width+x]]
			result += "\n"
		return result	

	def __repr__(self):
		return self.layerToStr(self.mergedImage)

#Execution stuff

def test1():
	image = Image("123456789012",3,2)
	print(image.layers)
	return

def test2():
	image = Image("0222112222120000",2,2)
	image.merge()
	print(image.mergedImage)
	return

def main():
	rawInput = open("./input/8.txt").read()
	print(part1(rawInput))
	print(part2(rawInput))
	return

test1()
test2()
main()