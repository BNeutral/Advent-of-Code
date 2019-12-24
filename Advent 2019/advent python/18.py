from collections import defaultdict
from util import *
import networkx as nx
import sys

#Problem code

def part1(stringData):
	maze = Maze(stringData)
	return maze.findMinPath()

def part2(stringData):
	maze = Maze(stringData, True)
	return maze.findMinPath()

def keySetToMask(keySet):
	result = 0
	for key in keySet:
		result |= keyCharToMask(key)
	return result

def keyCharToMask(char):
	return 1 << ord(char) - ord('a')

def isSubmask(mask, submask):
	return mask & submask == submask

def bits(mask):
    while mask:
        b = mask & (~mask+1)
        yield b
        mask ^= b

class Maze:

	def __init__(self, stringData, splitStarts=False):
		self.floorGraph = nx.Graph()
		self.stateGraph = nx.Graph()
		self.walkable = set()
		self.keys = {} #bitmask -> vector2
		self.doors = {} #bitmask -> vector2
		self.start = []
		self.paths = {} #[(start,end)] -> set(vector2)
		self.requirements = defaultdict(int)
		self.reachableStates = defaultdict(set)
		self.parseMaze(stringData, splitStarts)
		self.finalState = sum(list(self.keys))
		self.calculatePaths()
		self.calculateRequirements()
		self.calculateReachableStates()

	def editMazeStarts(self, splitData):
		for y in range(len(splitData)) :
			for x in range(len(splitData[y])):
				if splitData[y][x] == "@":
					splitData[y] =  splitData[y][0:x-1] + "###" + splitData[y][x+2:]
					splitData[y-1] =  splitData[y-1][0:x-1] + "@#@" + splitData[y-1][x+2:]
					splitData[y+1] =  splitData[y+1][0:x-1] + "@#@" + splitData[y+1][x+2:]
					return splitData

	def parseMaze(self, stringData, splitStarts=False):
		splitData = stringData.strip().split("\n")
		if splitStarts:
			splitData = self.editMazeStarts(splitData)
		for y in range(len(splitData)) :
			for x in range(len(splitData[y])):
				position = Vector2(x,y)
				character = splitData[y][x]
				if character == "#":
					continue
				else:
					self.addWalkalbe(self.floorGraph, self.walkable, position)
					if character == ".":
						continue
					if character == "@":
						self.start.append(position)
					elif character.islower():
						self.keys[keyCharToMask(character)] = position
					else:
						self.doors[keyCharToMask(character.lower())] = position

	def calculatePaths(self):
		keys = list(self.keys.keys())
		for key,keyPos in self.keys.items():
			counter = -1
			self.paths[(0,key)] = []
			for start in self.start:
				try:
					path = nx.shortest_path(self.floorGraph, start, keyPos)
					self.paths[(counter,key)] = set(path)
					self.paths[(0,key)].append(set(path))		
				except:
					pass	
				counter -= 1
		for x in range(len(keys)):
			for y in range(1+x,len(keys)):
				k1 = self.keys[keys[x]]
				k2 = self.keys[keys[y]]
				try:
					path = nx.shortest_path(self.floorGraph, k1, k2)
					self.paths[(keys[x],keys[y])] = set(path)
					self.paths[(keys[y],keys[x])] = set(path)
				except:
					pass

	def calculateRequirements(self):
		for key in self.keys.keys():
			self.requirements[key] |= 0
			for path in self.paths[0,key]:
				for doorKey,doorPos in self.doors.items():
					if doorPos in path:
						self.requirements[key] |= doorKey	
		oldLen = 0
		while oldLen != sum(list(self.requirements.values())):
			oldLen = sum(list(self.requirements.values()))
			toAdd = defaultdict(set)
			for mainKey,state in self.requirements.items():
				for key in bits(state):
					toAdd[self.requirements[mainKey]].add(self.requirements[key])
			for key1,aSet in toAdd.items():
				for key2 in aSet:
					self.requirements[key1] |= self.requirements[key2]
		#print(self.requirements)		

	def calculateReachableStates(self):
		visited = set()
		toVisit = set()
		toVisit.add(0)
		while len(toVisit) > 0:
			state = toVisit.pop()
			visited.add(state)
			for key in self.keys:
				keyIsReachable = isSubmask(state, self.requirements[key])
				if keyIsReachable:
					maskUnion = state|key
					if maskUnion != state :
						self.reachableStates[state].add(maskUnion)
					if maskUnion in visited:
						continue
					else:
						toVisit.add(maskUnion)
		#print(self.reachableStates)
		
	def addWalkalbe(self, floorGraph, walkable, position) :
		walkable.add(position)
		for adjacent in position.fourAdjacents():
			if adjacent in walkable:
				floorGraph.add_edge(position, adjacent)

	def findMinPath(self):
		graph = nx.Graph() #graph of (state,lastkey1,lastkey2,...,lastkeyn) -> nextstate
		visited = set()
		toVisit = set()
		toVisit.add( (0,-1,-2,-3,-4) )
		while len(toVisit) > 0:
			quintupleState = toVisit.pop()
			if quintupleState in visited:
					continue
			visited.add(quintupleState)
			state = quintupleState[0]
			nextStates = self.reachableStates[state]
			for x in range(len(self.start)):
				key = quintupleState[x+1]
				for nextState in nextStates:
					targetKey = state ^ nextState
					if (key, targetKey) not in self.paths:
						continue
					dist = len(self.paths[(key, targetKey)])-1
					if nextState == self.finalState:
						graph.add_edge( quintupleState, nextState, weight=dist)
					else:
						newQuintupleState = list(quintupleState)
						newQuintupleState[x+1] = targetKey
						newQuintupleState[0] |= targetKey
						newQuintupleState = tuple(newQuintupleState)
						graph.add_edge( quintupleState, newQuintupleState, weight=dist)
						toVisit.add(newQuintupleState)
		#path = nx.dijkstra_path(graph, (0,0), self.finalState)
		return nx.dijkstra_path_length(graph, (0,-1,-2,-3,-4), self.finalState)

#Execution stuff

def test1():
	rawInput = "########################\n#...............b.C.D.f#\n#.######################\n#.....@.a.B.c.d.A.e.F.g#\n########################\n"
	print(part1(rawInput)) #132
	rawInput = "#################\n#i.G..c...e..H.p#\n########.########\n#j.A..b...f..D.o#\n########@########\n#k.E..a...g..B.n#\n########.########\n#l.F..d...h..C.m#\n#################\n"
	print(part1(rawInput)) #136
	rawInput = "########################\n#@..............ac.GI.b#\n###d#e#f################\n###A#B#C################\n###g#h#i################\n########################\n"
	print(part1(rawInput)) #81
	return

def test2():
	rawInput = "#############\n#DcBa.#.GhKl#\n#.###...#I###\n#e#d#.@.#j#k#\n###C#...###J#\n#fEbA.#.FgHi#\n#############"
	print(part2(rawInput)) #32
	rawInput = "#############\n#g#f.D#..h#l#\n#F###e#E###.#\n#dCba...BcIJ#\n#####.@.#####\n#nK.L...G...#\n#M###N#H###.#\n#o#m..#i#jk.#\n#############\n"
	print(part2(rawInput)) #72


def main():
	rawInput = open("./input/18.txt").read()
	print("Computing, may take a while...")
	print("Part1: ",part1(rawInput))
	print("Part2: ",part2(rawInput))
	return

#test1()
#test2()
main()