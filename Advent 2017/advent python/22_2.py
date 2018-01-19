from enum import Enum
class Status(Enum):
	CLEAN = 0
	WEAK = 1
	INFECTED = 2
	FLAGGED = 3

class Virus:
	def __init__(self):
		self.facing = [0,1]
		self.facingNum = 0
		self.pos = (0,0)
		self.burstCounter = 0	
		self.orderX = [0,1,0,-1]
		self.orderY = [1,0,-1,0]

	def burst(self, grid):
		self.burstCounter += 1
		
	def move(self, grid):
		infectedSomething = False
		if (self.pos) in grid: #infected, gets cleaned
			status = grid[self.pos]
			if status == Status.INFECTED:
				self.turnRight()
				grid[self.pos] = Status.FLAGGED
			elif status == Status.WEAK:
				grid[self.pos] = Status.INFECTED
				infectedSomething = True
			else : #status == Status.FLAGGED:
				self.turnRight()
				self.turnRight()
				del grid[self.pos]			
		else: #not infected
			self.turnLeft()
			grid[self.pos] = Status.WEAK
		self.pos = (self.pos[0] + self.facing[0], self.pos[1] + self.facing[1])
		return infectedSomething

	def turnRight(self):
		self.facingNum = (self.facingNum+1)%4
		self.turnUpdate()
	
	def turnLeft(self):
		self.facingNum = (self.facingNum-1)%4
		self.turnUpdate()

	def turnUpdate(self):
		self.facing[0] = self.orderX[self.facingNum]
		self.facing[1] = self.orderY[self.facingNum]
	

def getData() :
	f = open("./input/input22","r")
	l = f.readline()
	size = (len(l)-1)/2
	f.seek(0)
	parsed = parse(f, size)
	f.close()
	return parsed

def parse(f,size):
	result = {}
	y = size
	for line in f:
		x = -size;
		for char in line:
			if char == '#' :
				result[(x,y)] = Status.INFECTED
			x += 1
		y -= 1
	return result

def main() :
	v = Virus()
	grid = getData()
	originalSet = set(grid)
	nicePrint(grid, (0,0), 12)
	cont = 0
	for x in range (0,10000000):
		if v.move(grid) :
			cont += 1
	print cont
		

def test():
	v = Virus()
	string = [".........",".........",".........",".....#...","...#.....",".........",".........","........."]
	grid = parse(string,4)
	cont = 0
	for x in range (0,100):
		if v.move(grid) :
			cont += 1
	nicePrint(grid, (0,0), 10)
	print cont

def nicePrint(grid, center, side) :
	c = "."
	for y in range (-side,side+1) :
		for x in range (-side,side+1) :
			pos = (x,-y)
			if pos in grid:
				status = grid[pos]
				if status == Status.INFECTED:
					print '#',
				elif status == Status.WEAK:
					print 'W',
				else : #status == Status.FLAGGED:
					print 'F',
			else :
				print '.',
		print ' '
				

main()
	
