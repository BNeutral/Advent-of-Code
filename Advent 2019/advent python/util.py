from collections import defaultdict
import re
import math

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

def arrayGDC(array):
	if len(array) <= 1:
		return array[0]
	return math.gcd(array[0],arrayGDC(array[1:]))

#Classes
class Vector2:

	tolerance = 0.000001

	def __init__(self, x, y):
		self.x = x
		self.y = y

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

	def copy(self):
		return Vector2(self.x,self.y)

	def angle(self):
		return math.atan2(self.x, self.y)

	def __eq__(self, other):
		return self.x==other.x and self.y==other.y

	def __hash__(self):
		return hash( (self.x,self.y) )

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