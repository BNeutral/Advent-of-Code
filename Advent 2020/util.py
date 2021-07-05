import math
import sys

#Parsing
def linesToInt(lines):
	return list(map(int,lines.trim().split("\n")))

def lineDigitsToArray(line):
	return list(map(int,line))

def commaSeparatedLineToInts(line):
	return list(map(int,line.split(",")))

#Math
def minimumCommonMultiple(array):
	mcm = array[0]
	for i in array[1:]:
		mcm = mcm*i//math.gcd(mcm, i)
	return mcm

#Finds the greatest common divisor of an array
def arrayGDC(array):
	if len(array) <= 1:
		return array[0]
	return math.gcd(array[0],arrayGDC(array[1:]))

#Used by modinv
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

#Taken from google
#Modinv is such that a*x % b = 1 => x = modinv(a,b)
#Note that multplying the found x by k, a*(kx) % b = k, but the found kx may need % b to be in range 
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

#Visualization

#printchars: Array with the character to use for each value the dict takes
#0 should be the empty char
#dict: Dictionary of vector2 positions
def drawDictScreen(dic, printchars=[" ","▓","░"], character=None):
	minx = sys.maxsize
	maxx = -sys.maxsize
	miny = sys.maxsize
	maxy = -sys.maxsize
	for vector in dic.keys():
		minx = min(vector.x,minx)
		miny = min(vector.y,miny)
		maxx = max(vector.x,maxx)
		maxy = max(vector.y,maxy)
	result = ""
	for y in range(miny,maxy+1):
		for x in range(minx,maxx+1):
			pos = Vector2(x,y)
			if character and pos == character:
				result += "X"
			else:
				if pos in dic:
					result += printchars[dic[pos]]
				else:
					result += " "
		result += "\n"
	return result	

def drawDictScreenSimple(dic):
	minx = sys.maxsize
	maxx = -sys.maxsize
	miny = sys.maxsize
	maxy = -sys.maxsize
	for vector in dic.keys():
		minx = min(vector.x,minx)
		miny = min(vector.y,miny)
		maxx = max(vector.x,maxx)
		maxy = max(vector.y,maxy)
	result = ""
	for y in range(miny,maxy+1):
		for x in range(minx,maxx+1):
			pos = Vector2(x,y)
			if pos in dic:
				result += str(dic[pos])
			else:
				result += " "
		result += "\n"
	return result	

def drawSet(s, chars=["#","O"], extraVectors=[]):
	minx = sys.maxsize
	maxx = -sys.maxsize
	miny = sys.maxsize
	maxy = -sys.maxsize
	for vector in s:
		minx = min(vector.x,minx)
		miny = min(vector.y,miny)
		maxx = max(vector.x,maxx)
		maxy = max(vector.y,maxy)
	result = ""
	for y in range(miny,maxy+1):
		for x in range(minx,maxx+1):
			pos = Vector2(x,y)
			if pos in extraVectors:
				result += chars[1]
			elif pos in s:
				result += chars[0]
			else:
				result += " "
		result += "\n"
	return result	

#Classes

#A class for finding cycles 
class CycleDetector:

	#state to match is an array of states
	#min repeats is the amount of times the state should repeat in a cycle to be considered
	def __init__(self, stateToMatch, minRepeats):
		self.initialState = stateToMatch
		self.stateLength = len(stateToMatch)
		self.sightings = []
		self.cycles = []
		self.minRepeats = minRepeats
		for _ in range(self.stateLength):
			self.sightings.append(set())
			self.cycles.append([])

	#Returns a list with the smallest cycles found
	def getCycles(self):
		smallestPeriods = []
		for i in range(self.stateLength):
			smallestPeriods.append(min(self.cycles[i]))
		return list(dict.fromkeys(smallestPeriods))

	#Given a new state, check repeats for each variable
	def giveInput(self, state, step):
		for i in range(self.stateLength):
			if state[i] == self.initialState[i]:
				self.sightings[i].add(step)
				cycleLength = step//self.minRepeats
				hasRepeated = True
				for x in range(1,self.minRepeats+1):
					if not cycleLength*(x) in self.sightings[i]:
						hasRepeated = False
						break
				if hasRepeated:
					self.cycles[i].append(cycleLength)	


#A 2 dimensional vector
class Vector2:
	
	def __init__(self, x, y):
		self.x = x
		self.y = y

	tolerance = 0.000001

	def add(self, other):
		return Vector2((self.x+other.x),(self.y+other.y))

	def sub(self, other):
		return Vector2((self.x-other.x),(self.y-other.y))

	def divScalar(self, scalar):
		return Vector2(self.x/scalar, self.y/scalar)

	def dotProduct(self, other):
		return self.x*other.x+self.y*other.y

	def length(self):
		return math.sqrt( math.pow(self.x,2) + math.pow(self.y,2))

	def normalize(self):
		if self.x == 0 and self.y == 0:
			return self.copy()
		return self.divScalar(self.length())

	def isSameDirectionColinear(self,other):
		arg = self.dotProduct(other) / (self.length()*other.length())
		return arg <= 1 + Vector2.tolerance and arg >= 1 - Vector2.tolerance

	def fourAdjacents(self):
		return [self.add(Vector2.up),self.add(Vector2.down),self.add(Vector2.left),self.add(Vector2.right)]

	def copy(self):
		return Vector2(self.x,self.y)

	def angle(self):
		return math.atan2(self.x, self.y)

	def __eq__(self, other):
		return self.x==other.x and self.y==other.y

	def __hash__(self):
		return hash( (self.x,self.y) )

	def __repr__(self):
		return str(self.x)+","+str(self.y)

Vector2.up = Vector2(0,-1)
Vector2.down = Vector2(0,1)
Vector2.left = Vector2(-1,0)
Vector2.right = Vector2(1,0)	
Vector2.zero = Vector2(0,0)	

class Vector3:

	tolerance = 0.000001

	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def add(self, other):
		return Vector3((self.x+other.x),(self.y+other.y),(self.z+other.z))

	def sub(self, other):
		return Vector3((self.x-other.x),(self.y-other.y),(self.z-other.z))

	def mulScalar(self, scalar):
		return Vector3(self.x*scalar, self.y*scalar, self.z*scalar)

	def divScalar(self, scalar):
		return Vector3(self.x/scalar, self.y/scalar, self.z/scalar)

	def dotProduct(self, other):
		return self.x*other.x+self.y*other.y+self.z*other.z

	def length(self):
		return math.sqrt( math.pow(self.x,2) + math.pow(self.y,2) + math.pow(self.z,2))

	def normalize(self):
		if self.x == 0 and self.y == 0 and self.z == 0:
			return self.copy()
		return self.divScalar(self.length())

	def fourAdjacents(self):
		return [self.add(Vector3.yup),self.add(Vector3.ydown),self.add(Vector3.xleft),self.add(Vector3.xright)]

	def copy(self):
		return Vector3(self.x, self.y, self.z)

	def __iter__(self):
		return iter((self.x, self.y, self.z))

	def __eq__(self, other):
		return self.x==other.x and self.y==other.y and self.z==other.z

	def __hash__(self):
		return hash( (self.x,self.y,self.z) )

	def __repr__(self):
		return str(self.x)+","+str(self.y)+","+str(self.z)

	def __delitem__(self, key):
		self.__delattr__(key)

	def __getitem__(self, key):
		if key == 0:
			return self.__getattribute__("x")
		if key == 1:
			return self.__getattribute__("y")
		if key == 2:
			return self.__getattribute__("z")
		else:
			return self.__getattribute__(key)

	def __setitem__(self, key, value):
		if key == 0:
			self.__setattr__("x", value)
		elif key == 1:
			self.__setattr__("y", value)
		elif key == 2:
			self.__setattr__("z", value)
		else:
			self.__setattr__(key, value)

Vector3.yup = Vector3(0,-1,0)
Vector3.ydown = Vector3(0,1,0)
Vector3.xleft = Vector3(-1,0,0)
Vector3.xright = Vector3(1,0,0)	
Vector3.zero = Vector3(0,0,0)	