from collections import defaultdict
import re
import math

def linesToInt(lines):
	return list(map(int,lines.trim().split("\n")))

def lineDigitsToArray(line):
	return list(map(int,line))

def commaSeparatedLineToInts(line):
	return list(map(int,line.split(",")))

class Vector2:

	tolerance = 0.000001

	def __init__(self, x, y):
		self.x = x
		self.y = y

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