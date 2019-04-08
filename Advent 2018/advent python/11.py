import sys

#Problem code

def solve(serial, minSquare, maxSquare):
	size = 300
	grid = [[0 for _ in range(size)] for _ in range(size)]
	populateGrid(grid, serial)
	summedAreaTable = SummedAreaTable(grid, size)
	currentMax = -sys.maxint
	for y in range(size):
		for x in range(size):
			for square in range(minSquare, maxSquare+1):
				square = min(square, size-1-y, size-1-x)
				sum = summedAreaTable.getSquare(x,y,square,square)
				if sum > currentMax:
					currentMax = sum
					maxX = x+1
					maxY = y+1
					squareSize = square
	return maxX,maxY,squareSize

def populateGrid(grid, serial):
	for y in range(len(grid)):
		for x in range(len(grid[y])):
			grid[y][x] = Cell(x+1,y+1).getPowerLevel(serial)

class SummedAreaTable:

	def __init__(self, grid, size):
		self.grid = grid
		self.table = [[0 for _ in range(size)] for _ in range(size)]
		for y in range(size):
			for x in range(size):
				value = grid[y][x]
				if y > 0:
					value += self.table[y-1][x]
				if x > 0:
					value += self.table[y][x-1]
				if y > 0 and x > 0:
					value -= self.table[y-1][x-1]
				self.table[y][x] = value

	def getSquare(self, topLeftX, topLeftY, lenX, lenY):
		topLeftX -= 1
		topLeftY -= 1
		topLeft = self.__getVal(topLeftX,topLeftY)
		topRight = self.__getVal(topLeftX+lenX,topLeftY)
		botLeft = self.__getVal(topLeftX,topLeftY+lenY)
		botRight = self.__getVal(topLeftX+lenX,topLeftY+lenY)
		return topLeft+botRight-topRight-botLeft

	def __getVal(self,x,y):
		if x < 0:
			return 0
		if y < 0:
			return 0
		return self.table[y][x]
			
class Cell:

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.powerLevel = None
		self.sumAhead = {}

	def getRackID(self):
		return self.x+10

	def getPowerLevel(self, serial):
		if self.powerLevel:
			return self.powerLevel
		level = self.getRackID()
		level *= self.y
		level += serial
		level *= self.getRackID()
		if level <100:
			self.powerLevel = -5
		else:
			self.powerLevel = ((level/100)%10) - 5
		return self.powerLevel

	def __repr__(self):
		return str(self.__dict__)

#Execution stuff

def test1():
	print(Cell(3,5).getPowerLevel(8))
	print(Cell(122,79).getPowerLevel(57))
	print(Cell(217,196).getPowerLevel(39))
	print(Cell(101,153).getPowerLevel(71))
	return

def test2():
	print(solve(18,3,3))
	print(solve(42,3,3))
	print(solve(18,1,300))
	print(solve(42,1,300))
	return

def test3():
	grid=[[31,2,4,33,5],[12,26,9,10,29],[13,17,21,22,20],[24,23,15,16,14],[30,8,28,27,11]]
	table = SummedAreaTable(grid,5)
	print(table.getSquare(0,0,1,1),31)
	print(table.getSquare(0,0,2,3),101)
	print(table.getSquare(0,0,5,3),254)
	print(table.getSquare(0,0,2,5),186)
	print(table.getSquare(0,0,5,5),450)
	print(table.getSquare(2,3,3,2),111)
	return


def main():
	print(solve(5153,3,3))
	print(solve(5153,1,300))
	return

main()
