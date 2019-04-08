import sys
import heapq

#Problem code

def part1(depth, targetX, targetY):
	_, danger = populateGrid(depth, targetX, targetY)
	return danger

#Apparently this is a bogus implementation, the grid needs to be calculated on demand since the paths to reach the target can be quite ridiculous
def populateGrid(depth, targetX, targetY):
	grid = []
	danger = 0
	for y in range(targetY+100):
		grid.append([])
		for x in range(targetX+100):
			cavePos = CavePosition(x, y, depth, grid, targetX, targetY)
			grid[y].append(cavePos)
			if x <= targetX and y <= targetY:
				danger += cavePos._type
	#printMap(grid, targetX, targetY)
	return grid, danger

def part2(depth, targetX, targetY):
	grid, _ = populateGrid(depth, targetX, targetY)
	distances = findDistances(grid, targetX, targetY)
	output = "Depth: "+str(depth)
	possibilities = []
	if (targetX,targetY,0) in distances:
		#output = output+" Reached with nothing :"+str(distances[(targetX,targetY,0)]+7)
		possibilities.append(distances[(targetX,targetY,0)]+7)
	if (targetX,targetY,1) in distances:
		#output = output+" Reached with torch :"+str(distances[(targetX,targetY,1)])
		possibilities.append(distances[(targetX,targetY,1)])
	if (targetX,targetY,2) in distances:
		#output = output+" Reached with climbing gear :"+str(distances[(targetX,targetY,2)]+7)
		possibilities.append(distances[(targetX,targetY,2)]+7)
	output = output+" Min Distance: "+str(min(possibilities))
	return output
	#return distances[grid[targetY][targetX]]

#Find min distances from current position in a poorly optimized way
def findDistances(grid, targetX, targetY):
	toVisit = PriorityQueue()
	toVisit.put((0,0,1),0)
	distances = {}
	distances[(0,0,1)] = 0
	while not toVisit.empty():
		nodeTuple = toVisit.get()
		currentCavePos = grid[nodeTuple[1]][nodeTuple[0]]
		currentDistance = distances[nodeTuple]
		currentTool = nodeTuple[2]
		currentValidTools = requiredTools(currentCavePos) 
		adjacents = currentCavePos.adjacentPositions()
		adjTuples = []
		for adj in adjacents:
			reqTools = requiredTools(adj) & currentValidTools
			for tool in reqTools:
				adjTuples.append((adj.x,adj.y,tool))
		for adj in adjTuples:
			dist = currentDistance + 1
			if currentTool != adj[2]:					
				dist += 7
			if adj not in distances or dist < distances[adj]:
				distances[adj] = dist
				toVisit.put(adj, dist)
	return distances

def requiredTools(cavePosition):
	posType = cavePosition.getType()
	if posType == 0: #Rock 1 or 2
		return set([1,2])
	if posType == 1: #Wet 0 or 2
		return set([0,2])
	if posType == 2: #Narrow 0 or 1
		return set([0,1])

def printMap(grid, targetX, targetY):
	for y in range(len(grid)):
		for x in range(len(grid[y])):
			if y == 0 and x == 0:
				sys.stdout.write("M")
			elif y == targetY and x == targetX:
				sys.stdout.write("T")
			else:
				sys.stdout.write(str(grid[y][x]))
		sys.stdout.write("\n")
		sys.stdout.flush()
	sys.stdout.flush()

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

class CavePosition:

	def __init__(self, x, y, depth, grid, targetX, targetY):
		self.grid = grid
		self.depth = depth
		self.x = x
		self.y = y
		self.targetX = targetX
		self.targetY = targetY
		self._geoIndex = None
		self._erosionLevel = None
		self._type = None
		self.getType()

	def isTarget(self):
		return self.x == self.targetX and self.y == self.targetY

	def getGeoIndex(self):
		if self._geoIndex:
			return self._geoIndex
		elif self.x == 0 and self.y == 0:
			self._geoIndex = 0
		elif self.isTarget():
			self._geoIndex = 0
		elif self.y == 0:
			self._geoIndex = self.x*16807
		elif self.x == 0:
			self._geoIndex = self.y*48271
		else:
			self._geoIndex = self.grid[self.y][self.x-1].getErosionLevel() * self.grid[self.y-1][self.x].getErosionLevel()
		return self._geoIndex

	def getErosionLevel(self):
		if self._erosionLevel:
			return self._erosionLevel
		else:
			self._erosionLevel = (self.getGeoIndex()+self.depth)%20183
		return self._erosionLevel

	def getType(self):
		if self._type:
			return self._type
		else:
			self._type = self.getErosionLevel() % 3
		return self._type

	def up(self):
		if self.y == 0:
			return None
		return self.grid[self.y-1][self.x]

	def down(self):
		if self.y == len(self.grid)-1:
			return None
		return self.grid[self.y+1][self.x]

	def left(self):
		if self.x == 0:
			return None
		return self.grid[self.y][self.x-1]

	def right(self):
		if self.x == len(self.grid[0])-1:
			return None
		return self.grid[self.y][self.x+1]

	def adjacentPositions(self):
		positions = []
		for pos in [self.up(), self.left(), self.right(), self.down()]:
			if pos:
				positions.append(pos)
		return positions

	def __repr__(self):
		if self._type == 0:
			return "." # rocky
		elif self._type == 1:
			return "=" # wet
		elif self._type == 2:
			return "|" # narrow
		else:
			return "?"

	def __hash__(self):
		return hash( (self.x,self.y) )

	def __eq__(self, another):
		return self.x == another.x and self.y == another.y

#Execution stuff

def test1():
	print(part1(510,10,10))
	print(part1(20,30,30))
	print(part1(0,30,30))
	print(part1(50,30,30))
	print(part1(200,30,30))
	print(part1(1000,30,30))	
	return

def test2():
	print(part2(510,10,10))
	print(part2(20,30,30))
	#print(part2(0,30,30)) Breaks since I made the grid bigger for some reason
	print(part2(50,30,30))
	print(part2(200,30,30))
	print(part2(1000,30,30))
	return

def main():
	print(part1(7863,14,760))
	print(part2(7863,14,760))
	return

#test1()
#test2()
main()
