import re
import sys
#GLPK solution attempt, which I never finished as I had to revisit my LP knowledge and lost interest midway

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

def toGLPK(bots):
	minX, maxX, minY, maxY, minZ, maxZ = findMinMax(bots)
	print "### VARIABLES ####################################"
	print "set BOTS"
	print "var X, integer;"
	print "var Y, integer;"
	print "var Z, integer;"
	print "var INRANGE{i in BOTS} >= 0, binary;"
	print "### MODEL ####################################"
	print "maximize R: sum{i in BOTS} INRANGE[i];"
	#print "subject to"
	print "s. t. xTop{i in BOTS} X <= ( RB[i] + XB[i] ) * INRANGE[i] + ( 1 - INRANGE[i] ) * "+str(maxX)+";"
	print "s. t. xBot{i in BOTS} X >= ( RB[i] - XB[i] ) * INRANGE[i] + ( 1 - INRANGE[i] ) * "+str(minX)+";"
	print "s. t. yTop{i in BOTS} Y <= ( RB[i] + YB[i] ) * INRANGE[i] + ( 1 - INRANGE[i] ) * "+str(maxY)+";"
	print "s. t. yBot{i in BOTS} Y >= ( RB[i] - YB[i] ) * INRANGE[i] + ( 1 - INRANGE[i] ) * "+str(minY)+";"
	print "s. t. zTop{i in BOTS} Z <= ( RB[i] + YB[i] ) * INRANGE[i] + ( 1 - INRANGE[i] ) * "+str(maxZ)+";"
	print "s. t. zBot{i in BOTS} Z >= ( RB[i] - YB[i] ) * INRANGE[i] + ( 1 - INRANGE[i] ) * "+str(minZ)+";"

	#print "bounds"
	#print str(minX)+" <= X <= "+str(maxX)+";"
	#print str(minY)+" <= Y <= "+str(maxY)+";"
	#print str(minZ)+" <= Z <= "+str(maxZ)+";"
	print "### DATA #####################################"
	print "data;"
	line = "set BOTS:= "
	for bot in bots:
		line = line + "B" + str(bot.id) + " "
	print line
	print "param botp: XB YB ZB RB :="
	for bot in bots:
		print "B" + str(bot.id),bot.x,bot.y,bot.z,bot.r 
	print "end;"

	
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

	id = 0

	def __init__(self, string=None, x=0, y=0, z=0, r=0):
		regex = re.compile(r'pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)')
		match = regex.match(string)
		self.x = int(match.group(1))
		self.y = int(match.group(2))
		self.z = int(match.group(3))
		self.r = int(match.group(4))
		self.id = Nanobot.id
		Nanobot.id += 1

def test():
	rawInput = "pos=<10,12,12>, r=2\npos=<12,14,12>, r=2\npos=<16,12,12>, r=4\npos=<14,14,14>, r=6\npos=<50,50,50>, r=200\npos=<10,10,10>, r=5"
	bots = dataToParsedArray(rawInput)
	toGLPK(bots)
	return

def main():
	rawInput = open("./input/23.txt","r").read()
	bots = dataToParsedArray(rawInput)
	print(toGLPK(bots))

#Create GLPK file for problem solving
#Run this file and redirect the stdout to a file
#Then run glpsol -m "filename"
#Read the activity values to find the solution
test()
