#urld
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
			self.turnRight()
			grid.remove(self.pos)
		else: #not infected
			self.turnLeft()
			grid.add(self.pos)
			infectedSomething = True
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
	result = set()
	y = size
	for line in f:
		x = -size;
		for char in line:
			if char == '#' :
				result.add((x,y))
			x += 1
		y -= 1
	return result

def main() :
	v = Virus()
	grid = getData()
	originalSet = set(grid)
	nicePrint(grid, (0,0), 12)
	cont = 0
	for x in range (0,10000):
		if v.move(grid) :
			cont += 1
	print cont
		

def test():
	v = Virus()
	string = ["..#","#..","..."]
	grid = parse(string,1)
	print(grid)
	v.move(grid)
	print(grid)
	return

def test2():
	v = Virus()
	print(v.facing)
	v.turnRight()
	print(v.facing)
	v.turnRight()
	print(v.facing)
	v.turnRight()
	print(v.facing)
	v.turnRight()
	return
	
def test3():
	v = Virus()
	string = [".........",".........",".........",".....#...","...#.....",".........",".........","........."]
	grid = parse(string,4)
	print grid
	nicePrint(grid, v.pos, 3)
	for x in range (0,6):
		print v.move(grid)
		print "beforeMove"
		print "pos"
		print v.pos
		print v.pos[0]+v.facing[0]
		print v.pos[1]+v.facing[1]
		print "facing"
		print v.facing
		nicePrint(grid, (0,0), 3)
		print grid
	return

def test4():
	v = Virus()
	string = [".........",".........",".........",".....#...","...#.....",".........",".........","........."]
	grid = parse(string,4)
	cont = 0
	for x in range (0,70):
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
				print '#',
			else :
				print '.',
		print ' '
				

main()
	
