from collections import defaultdict
import re
import sys
import copy

#File parsing stuff
def dataToParsedArray(stringData) :
	split =  stringData.split("\n")
	tracks = [[" " for _ in range(len(split[0]))] for _ in range(len(split))]
	carts = []
	for y in range(len(split)):
		for x in range(len(split[0])):
			char = split[y][x]
			tracks[y][x] = char
			if char == ">":
				tracks[y][x] = "-"
				carts.append(Cart(complex(x,y),1,tracks))
			elif char == "^":
				tracks[y][x] = "|"
				carts.append(Cart(complex(x,y),0-1j,tracks))
			elif char == "v":
				tracks[y][x] = "|"
				carts.append(Cart(complex(x,y),0+1j,tracks))
			elif char == "<":
				tracks[y][x] = "-"
				carts.append(Cart(complex(x,y),-1,tracks))
	return tracks,carts

#Problem code

def printTracks(tracks):
	for y in tracks:
		for x in y:
			sys.stdout.write(x)
		sys.stdout.write("\n")
		sys.stdout.flush()
	sys.stdout.flush()

def printTracksAndCarts(tracks, carts):
	cp = copy.deepcopy(tracks)
	for cart in carts:
		cp[cart.pos[1]][cart.pos[0]] = str(cart)
	printTracks(cp)

def part1(tracks,carts):
	while True:
		carts.sort()
		for cart in carts:
			cart.advance()
			collided,cart1,cart2 = justCollided(cart,carts)
			if collided:
				return cart1.pos

def part2(tracks,carts):
	while len(carts) > 1:
		carts.sort()
		x = 0
		while x < len(carts):
			cart = carts[x]
			cart.advance()
			collided,cart1,cart2 = justCollided(cart,carts)
			if collided:
				i1 = carts.index(cart1)
				i2 = carts.index(cart2)
				carts.remove(cart1)
				carts.remove(cart2)
				if i1 < x or i2 < x:
					x -= 1
			else:
				x += 1
	return carts[0].pos

def justCollided(mainCart, carts):
	for cart in carts:
		if not mainCart is cart:
			if mainCart.collides(cart):
				return True, mainCart, cart
	return False,None,None

class Cart:

	facingDict = { 1 : ">", -1:"<", 0+1j : "v", 0-1j : "^" }

	def __init__(self, pos, facing, tracks):
		self.pos = pos
		self.facing = facing
		self.turnCounter = 0
		self.tracks = tracks

	def advance(self):
		self.pos = self.pos + self.facing
		self.checkPosition()

	def __getTrackTile(self):
		return self.tracks[int(self.pos.imag)][int(self.pos.real)]

	def checkPosition(self):
		posInTrack = self.__getTrackTile()
		if posInTrack == "+":
			times = self.turnCounter % 3
			if times == 0:
				self.turnLeft()
			elif times == 2:
				self.turnRight()
			self.turnCounter += 1
		elif posInTrack == "/":
			if self.facing.real == 0:
				self.turnRight()
			else :
				self.turnLeft()
		elif posInTrack == "\\":
			if self.facing.real == 0:
				self.turnLeft()
			else :
				self.turnRight()

	def turnRight(self):
		self.facing = complex(-self.facing.imag,self.facing.real)

	def turnLeft(self):
		self.facing = complex(self.facing.imag,-self.facing.real)

	def collides(self,other):
		return self.pos == other.pos

	def __repr__(self):
		return Cart.facingDict[self.facing]

	def __cmp__(self, other):
		if self.pos.imag != other.pos.imag:
			if self.pos.imag < other.pos.imag:
				return -1
			else:
				return 1
		elif self.pos.real != other.pos.real:
			if self.pos.real < other.pos.real:
				return -1
			else:
				return 1
		else:
			return 0

#Execution stuff

def test1():
	rawInput = "/->-\        \n|   |  /----\\\n| /-+--+-\  |\n| | |  | v  |\n\-+-/  \-+--/\n  \------/   "
	tracks,carts = dataToParsedArray(rawInput)
	print(part1(tracks,carts))
	return

def test2():
	rawInput = "/>-<\  \n|   |  \n| /<+-\\\n| | | v\n\>+</ |\n  |   ^\n  \<->/"
	tracks,carts = dataToParsedArray(rawInput)
	print(part2(tracks, carts))
	return

def main():
	rawInput = open("./input/13.txt").read()
	tracks,carts = dataToParsedArray(rawInput)
	print(part1(tracks,carts))
	tracks,carts = dataToParsedArray(rawInput)
	print(part2(tracks,carts))
	return

test1()
test2()
main()
