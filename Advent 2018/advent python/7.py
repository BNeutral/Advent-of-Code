import re

#File parsing stuff
def dataToParsedArray(stringData) :
	result = [] 
	for line in stringData.split("\n"):
		line = line.strip()
		if line != "":
			result.append(parse(line))
	return result

def parse(line) :
	return line

#Problem code

def part1(data):
	graph = Graph()
	for line in data:
		graph.parseLine(line, 0)
	graph.findFirst()
	return "".join(graph.alphabeticFirstSearch())


def part2(data, workers, baseTime):
	graph = Graph()
	for line in data:
		graph.parseLine(line, baseTime)
	graph.findFirst()
	return graph.timedSearch(workers)

class Graph:

	regex = re.compile(r'Step (\w+) must be finished before step (\w+) can begin.')

	def __init__(self):
		self.id = id
		self.nodes = {}
		self.nodeIDs = set()
		self.endNodes = set()
		self.startNodes = []

	def parseLine(self, string, baseTime):
		match = self.regex.match(string)
		nodeID1 = match.group(1)
		nodeID2 = match.group(2)
		node1 = self.addIfNotIn(nodeID1, baseTime)
		node2 = self.addIfNotIn(nodeID2, baseTime)
		node1.addConnection(node2)
		self.nodeIDs.add(nodeID1)
		self.nodeIDs.add(nodeID2)
		self.endNodes.add(nodeID2)
		return

	def addIfNotIn(self, nodeID, baseTime):
		if not (nodeID in self.nodes):
			self.nodes[nodeID] = Node(nodeID, baseTime)
		return self.nodes[nodeID]

	def findFirst(self):
		self.startNodes = list(self.nodeIDs.difference(self.endNodes))

	def alphabeticFirstSearch(self):
		result = []
		available = self.startNodes
		while len(available) > 0:
			available.sort()
			node = self.nodes[available.pop(0)]
			if node.canBeVisited():
				node.visit()
				result.append(node.id)
				for nextNode in node.connectsTo:
					available.append(nextNode.id)
		return result

	def timedSearch(self, workers):
		time = 0
		result = []
		available = self.startNodes
		visited = 0
		while visited < len(self.nodes):
			available.sort()
			time += 1
			for id in available:
				node = self.nodes[id]
				if workers > 0 and node.pendingWorker():
					workers -= 1
					node.hasWorker = True
			for id in available:
				node = self.nodes[id]
				if node.canBeWorked():
					node.work()
				if node.canBeVisitedWorked():
					node.visit()
					workers += 1
					visited += 1
					result.append(node.id)
					for nextNode in node.connectsTo:
						if nextNode.id not in available:
							available.append(nextNode.id)
		return result, time

class Node:

	def __init__(self, id, baseTime):
		self.id = id
		self.connectsTo = set()
		self.connectionCounter = 0
		self.connectionsNeeded = 0
		self.visited = False
		self.timeCounter = baseTime + ord(id)-64
		self.hasWorker = False

	def addConnection(self, otherNode):
		self.connectsTo.add(otherNode)
		otherNode.connectionsNeeded += 1

	def visit(self):
		self.visited = True
		self.hasWorker = False
		for node in self.connectsTo:
			node.connectionCounter += 1

	def canBeVisited(self):
		return not self.visited and self.connectionCounter == self.connectionsNeeded

	def pendingWorker(self):
		return not self.visited and self.canBeVisited() and not self.hasWorker

	def canBeWorked(self):
		return self.canBeVisited() and self.hasWorker

	def work(self):
		self.timeCounter -= 1

	def canBeVisitedWorked(self):
		return self.canBeVisited() and self.timeCounter <= 0

	def __repr__(self):
		return str(self.__dict__)

#Execution stuff

def test1():
	string = "Step C must be finished before step A can begin.\nStep C must be finished before step F can begin.\nStep A must be finished before step B can begin.\nStep A must be finished before step D can begin.\nStep B must be finished before step E can begin.\nStep D must be finished before step E can begin.\nStep F must be finished before step E can begin."
	data = dataToParsedArray(string)
	print(part1(data))
	return

def test2():
	string = "Step C must be finished before step A can begin.\nStep C must be finished before step F can begin.\nStep A must be finished before step B can begin.\nStep A must be finished before step D can begin.\nStep B must be finished before step E can begin.\nStep D must be finished before step E can begin.\nStep F must be finished before step E can begin."
	data = dataToParsedArray(string)
	print(part2(data,2,0))
	return

def main():
	rawInput = open("./input/7.txt").read()
	data = dataToParsedArray(rawInput)
	print(part2(data,4,60))
	return

main()
