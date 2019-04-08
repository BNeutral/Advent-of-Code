import re

#File parsing stuff
def parseString(string):
	regex = re.compile(r'(\d+) players; last marble is worth (\d+) points')
	match = regex.match(string.strip())
	return int(match.group(1)), int(match.group(2))

#Problem code
def part1(players, lastMarble):
	playerScores = [0 for _ in range(players)]
	currentPlayer = 0
	marbles = LinkedList()	
	for marbleValue in range(1,lastMarble+1):
		if marbleValue % 23 == 0:
			playerScores[currentPlayer] += marbleValue
			playerScores[currentPlayer] += marbles.popBehind(6)
		else :
			marbles.insertAhead(marbleValue,2)
		currentPlayer = (currentPlayer + 1) % players
		#marbles.printit()
	return max(playerScores)

def part2(players, lastMarble):
	return part1(players,lastMarble*100)

class LinkedList:

	def __init__(self):
		self.root = Node(0, None, None)
		self.root.next = self.root
		self.root.prev = self.root
		self.currentNode = self.root

	def printit(self):
		start = self.root
		string = "0"
		next = start.next
		while next != start:
			string += " "+str(next.value)
			next = next.next
		print(string)

	def popBehind(self, offset):
		for _ in range(offset):
			self.currentNode = self.currentNode.prev
		node = self.currentNode
		node.next.prev = node.prev
		node.prev.next = node.next
		self.currentNode = node.prev
		return node.value

	def insertAhead(self, value, offset):
		for _ in range(offset):
			self.currentNode = self.currentNode.next
		newNode = Node(value, self.currentNode, self.currentNode.next) 
		self.currentNode.next.prev = newNode
		self.currentNode.next = newNode

class Node:
	def __init__(self, value, prev, next):
		self.value = value
		self.prev = prev
		self.next = next

#Execution stuff
def test1():
	print(part1(9, 25))

def test2():
	print(part1(10, 1618) == 8317)
	print(part1(13, 7999) == 146373)
	print(part1(17, 1104) == 2764)
	print(part1(21, 6111) == 54718)
	print(part1(30, 5807) == 37305)
	return

def main():
	rawInput = open("./input/9.txt").read()
	players, last = parseString(rawInput)
	print(part2(players, last))
	return

main()
