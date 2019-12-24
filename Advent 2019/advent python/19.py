from util import *
from intcode import Interpreter

#Problem code

def part1(data):
	grid = generateGrid(data, 50)
	#print(drawSet(grid))
	return len(grid)

def generateGrid(data, gridSizeMax = 1200, yBlockSize = 10):
	#print("Generating", gridSizeMax)
	grid = set()
	x = 0
	startY = 0
	while x < gridSizeMax:
		#if x % 100 == 0:
			#print("Generated",x)
		while Vector2(x-1, startY) not in grid and x > 5:
			startY += 1
		y = startY
		hadOutput = True
		outputCounter = 0
		while hadOutput:
			#print(x,y,startY,yBlockSize)
			if outputCounter > 1:
				yBlockSize += 2
			programs = []
			threads = []
			positions = []
			hadOutput = False
			for z in range(y, y+yBlockSize):
				pos = Vector2(x,z)
				program = Interpreter(data, [], False)
				program.inputs.put(pos.x)
				program.inputs.put(pos.y)
				programs.append(program)
				positions.append(pos)
				threads.append(program.runInThread())
			for a in range(len(threads)):
				output = programs[a].output.get()
				if output == 1:
					hadOutput = True
					pos = positions[a]
					grid.add(pos)	
				threads[a].join()
			if hadOutput:
				outputCounter += 1
			y += yBlockSize
		x += 1
	return grid

def part2(data):
	grid = generateGrid(data)
	#print("Grid generated, length:",len(grid))
	return  findSquare(grid, 100)

def findSquare(grid, squaresize = 100):
	toVisit = list(grid)
	toVisit.sort(key=lambda x: x.x+x.y)
	#print("List sorted")
	squareMove = squaresize - 1
	for pos in toVisit:
		v1 = Vector2(pos.x, pos.y+squareMove)
		v2 = Vector2(pos.x+squareMove, pos.y)
		if v1 in grid and v2 in grid:
			#print(pos.x,pos.y)
			#dset = set()
			#dset.add(pos)
			#dset.add(v1)
			#dset.add(v2)
			#dset.add(v3)
			#print(drawSet(grid, extraVectors=dset))
			return pos.x*10000+pos.y

def main():
	rawInput = open("./input/19.txt").read()
	data = commaSeparatedLineToInts(rawInput)
	print("Computing, may take a long while. Could be optimized but I'm lazy.")
	print("Part1:",part1(data))
	print("Part2:",part2(data))
	return

#testCounting()
main()