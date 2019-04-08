import re
import sys
from z3 import *
#Actually failed to solve this problem properly so ended up using a solver, since it was the only solution I could find that didn't fail due to local minima

#File parsing stuff
def dataToParsedArray(stringData) :
	result = [] 
	for line in stringData.split("\n"):
		line = line.strip()
		if line != "":
			result.append(parse(line))
	return result

def parse(line) :
	return Nanobot(line)

#Problem code
def part1(bots):
	maxR = 0
	maxBot = None
	for bot in bots:
		if bot.r > maxR:
			maxR = bot.r
			maxBot = bot
	counter = 0
	for bot in bots:
		if maxBot.inRange(bot):
			counter += 1
	return maxBot, maxR, counter

def dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2])

def z3_abs(x):
    return If(x >= 0,x,-x)

def z3_dist(p1, p2):
    return z3_abs(p1[0] - p2[0]) + z3_abs(p1[1] - p2[1]) + z3_abs(p1[2] - p2[2])

def part2(bots):
    data = [(bot.r, (bot.x,bot.y,bot.z) ) for bot in bots]
    m = max(data)
    in_range = [x for x in data if dist(x[1], m[1]) <= m[0]]
    x = Int('x')
    y = Int('y')
    z = Int('z')
    orig = (x, y, z)
    cost_expr = x * 0
    for r, pos in data:
        cost_expr += If(z3_dist(orig, pos) <= r, 1, 0)
    opt = Optimize()
    opt.maximize(cost_expr)
    opt.check()
    result = opt.model()
    return "Distance:",dist( (0,0,0), (result[x].as_long(),result[y].as_long(),result[z].as_long()) )

#def poorMansPart2(bots, divisor):
#	lookup = {}
#	for bot in bots:
#		lookup[bot.id] = bot
#	minX = Nanobot.minX / divisor
#	maxX = Nanobot.maxX / divisor
#	minY = Nanobot.minY / divisor
#	maxY = Nanobot.maxY / divisor
#	minZ = Nanobot.minZ / divisor
#	maxZ = Nanobot.maxZ / divisor
#	bestSpots = []
#	bestInRange = 0
#	bestDistance = sys.maxint
#	while divisor >= 1:
#		bestSpots = []
#		bestInRange = 0
#		bestDistance = sys.maxint
#		print divisor
#		divBots = copy.deepcopy(bots)
#		for bot in divBots:
#			bot.x /= divisor
#			bot.y /= divisor
#			bot.z /= divisor
#			bot.r /= divisor
#			#print bot
#		print minX, maxX, minY, maxY, minZ, maxZ
#		for x in range(minX, maxX+1):
#			for y in range(minY, maxY+1):
#				for z in range(minZ, maxZ+1):
#					inRange = 0
#					inRangeID = []
#					distanceToOrigin = abs(x)+abs(y)+abs(z)
#					for bot in divBots:
#						if bot.inRangePos(x,y,z):
#							inRange += 1
#							inRangeID.append(bot.id)
#					if inRange > bestInRange:
#						bestDistance = distanceToOrigin
#						bestInRange = inRange
#						bestSpots = [(x,y,z)]
#					if inRange == bestInRange:
#						if distanceToOrigin < bestDistance:
#							bestDistance = distanceToOrigin
#							bestSpots = [(x,y,z)]
#						else:
#							bestSpots.append((x,y,z))
#		print len(bestSpots), bestInRange, bestDistance
#		#minX = ((min(bestSpots, key = lambda t: t[0])[0]))*10
#		#maxX = ((max(bestSpots, key = lambda t: t[0])[0])+1)*10
#		#minY = ((min(bestSpots, key = lambda t: t[1])[1]))*10
#		#maxY = ((max(bestSpots, key = lambda t: t[1])[1])+1)*10
#		#minZ = ((min(bestSpots, key = lambda t: t[2])[2]))*10
#		#maxZ = ((max(bestSpots, key = lambda t: t[2])[2])+1)*10
#		minX = (bestSpots[0][0]-10)*10
#		maxX = (bestSpots[0][0]+10)*10
#		minY = (bestSpots[0][1]-10)*10
#		maxY = (bestSpots[0][1]+10)*10
#		minZ = (bestSpots[0][2]-10)*10
#		maxZ = (bestSpots[0][2]+10)*10
#		divisor /= 10
#	return bestSpots, bestInRange, bestDistance
#	# 69632446 too low

#def recursivePart2(bots):
#	minX, maxX, minY, maxY, minZ, maxZ = findMinMax(bots)
#	startRadius = max(abs(maxX-minX),abs(maxY-minY),abs(maxZ-minZ)) 
#	currentBot = Nanobot(None, 0,0,0, startRadius)
#	bestRange = 0
#	while currentBot.r > 1:
#		print (currentBot.x, currentBot.y, currentBot.z),bestRange,currentBot.distancePos(0,0,0)
#		split = currentBot.split()
#		for splitbot in split:
#			counter = 0
#			for bot in bots:
#				if splitbot.inExtendedRange(bot):
#					counter += 1
#			if counter >= bestRange:
#				bestRange = counter
#				currentBot = splitbot
#	return (currentBot.x, currentBot.y, currentBot.z),bestRange,currentBot.distancePos(0,0,0)

#def recursivePart2(bots):
#	minX, maxX, minY, maxY, minZ, maxZ = findMinMax(bots)
#	startRadius = max(abs(maxX-minX),abs(maxY-minY),abs(maxZ-minZ)) 
#	toVisit = PriorityQueue()
#	toVisit.put(Nanobot(None, 0,0,0, startRadius),0)
#	while True:
#		currentBot = toVisit.get()
#		if currentBot.r <= 1:
#			break
#		split = currentBot.split()
#		for splitbot in split:
#			counter = 0
#			for bot in bots:
#				if splitbot.inRange(bot):
#					counter += 1
#			toVisit.put(splitbot, -counter)
#	return currentBot,currentBot.distancePos(0,0,0)

def findMinMax(bots):
	minX = sys.maxint
	minY = sys.maxint
	minZ = sys.maxint
	maxX = -sys.maxint
	maxY = -sys.maxint
	maxZ = -sys.maxint
	for bot in bots:
		maxX = max(maxX, bot.x)
		maxY = max(maxY, bot.y)
		maxZ = max(maxZ, bot.z)
		minX = min(minX, bot.x)
		minY = min(minY, bot.y)
		minZ = min(minZ, bot.z)
	return minX, maxX, minY, maxY, minZ, maxZ

class Nanobot:

	maxX = -sys.maxint
	minX = sys.maxint
	maxY = -sys.maxint
	minY = sys.maxint
	maxZ = -sys.maxint
	minZ = sys.maxint
	id = 0

	def __init__(self, string=None, x=0, y=0, z=0, r=0):
		if string:
			regex = re.compile(r'pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)')
			match = regex.match(string)
			self.x = int(match.group(1))
			self.y = int(match.group(2))
			self.z = int(match.group(3))
			self.r = int(match.group(4))
		else:
			self.x = x
			self.y = y
			self.z = z
			self.r = r
		Nanobot.maxX = max(Nanobot.maxX, self.x)
		Nanobot.maxY = max(Nanobot.maxY, self.y)
		Nanobot.maxZ = max(Nanobot.maxZ, self.z)
		Nanobot.minX = min(Nanobot.minX, self.x)
		Nanobot.minY = min(Nanobot.minY, self.y)
		Nanobot.minZ = min(Nanobot.minZ, self.z)
		self.id = Nanobot.id
		Nanobot.id += 1

	def inExtendedRange(self, other):
		return self.distance(other) <= self.r+other.r

	def inRange(self, other):
		return self.distance(other) <= self.r

	def inRangePos(self, x, y, z):
		return self.distancePos(x,y,z) <= self.r

	def distance(self, other):
		return abs(self.x-other.x)+abs(self.y-other.y)+abs(self.z-other.z)

	def distancePos(self, x, y, z):
		return abs(self.x-x)+abs(self.y-y)+abs(self.z-z)

	def split(self):
		newBots = []
		quarterR = int(self.r/4)
		splitBotR = int(self.r*0.75)
		newBots.append(Nanobot(None, self.x+quarterR, self.y, self.z, splitBotR))
		newBots.append(Nanobot(None, self.x-quarterR, self.y, self.z, splitBotR))
		newBots.append(Nanobot(None, self.x, self.y+quarterR, self.z, splitBotR))
		newBots.append(Nanobot(None, self.x, self.y-quarterR, self.z, splitBotR))
		newBots.append(Nanobot(None, self.x, self.y, self.z+quarterR, splitBotR))
		newBots.append(Nanobot(None, self.x, self.y, self.z-quarterR, splitBotR))
		return newBots

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y and self.z == other.z and self.r == other.r

	def __repr__(self):
		return str(self.__dict__)

	def __hash__(self):
		return hash( (self.x,self.y, self.z, self.r) )

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

#Execution stuff

def test():
	rawInput = "pos=<10,12,12>, r=2\npos=<12,14,12>, r=2\npos=<16,12,12>, r=4\npos=<14,14,14>, r=6\npos=<50,50,50>, r=200\npos=<10,10,10>, r=5"
	bots = dataToParsedArray(rawInput)
	print(part2(bots))
	return

def main():
	rawInput = open("./input/23.txt","r").read()
	bots = dataToParsedArray(rawInput)
	#print(part1(bots))
	print(part2(bots))
	return

#test()
main()
