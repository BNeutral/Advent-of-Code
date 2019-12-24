from collections import defaultdict
from util import *
import networkx as nx
import string

#File parsing stuff
def dataToGraph(stringData) :
	textGrid = stringData.split("\n")
	graph = nx.Graph()
	floor = set()
	letterPositions = {}
	letters = set(string.ascii_uppercase)
	portals = defaultdict(list)
	width = len(textGrid[0])
	height = len(textGrid)
	for y in range(height):
		for x in range(width):
			pos = Vector2(x,y)
			character = textGrid[y][x]
			if character == ".":
				floor.add(pos)
			elif character in letters:
				letterPositions[pos] = character
	for pos in floor:
		for adj in pos.fourAdjacents():
			if adj in floor:
				graph.add_edge(pos,adj)
			if adj in letterPositions:
				portalName = findPortalName(adj, letterPositions)
				portals[portalName].append(pos)	
				if portalName == "AA":
					start = pos
				if portalName == "ZZ":
					end = pos
	for pairs in portals.values():
		if len(pairs) > 1:
			graph.add_edge(pairs[0],pairs[1])
	return graph, start, end

def dataTo3DGraph(stringData) :
	textGrid = stringData.split("\n")
	graph = nx.Graph()
	floor = set()
	letterPositions = {}
	letters = set(string.ascii_uppercase)
	portals = defaultdict(list)
	width = len(textGrid[0])
	height = len(textGrid)
	for y in range(height):
		for x in range(width):
			pos = Vector3(x,y,0)
			character = textGrid[y][x]
			if character == ".":
				floor.add(pos)
			elif character in letters:
				pos2D = Vector2(pos.x, pos.y)
				letterPositions[pos2D] = character
	maxRecursionDepth = len(letterPositions) // 4
	for pos in floor:
		for depth in range(maxRecursionDepth):
			pos = pos.copy()
			pos.z = depth
			for adj in pos.fourAdjacents():
				if Vector3(adj.x, adj.y, 0) in floor:
					graph.add_edge(pos,adj)
				twoDAdj = Vector2(adj.x, adj.y)
				if twoDAdj in letterPositions:					
					portalName = findPortalName(twoDAdj, letterPositions)
					if depth == 0:
						if portalName == "AA":
							start = pos
						if portalName == "ZZ":
							end = pos
					inner = isInner(pos, width, height)
					if inner:
						portals[portalName+str(depth+1)].append(pos)
					elif depth != 0:	
						portals[portalName+str(depth)].append(pos)
	for pairs in portals.values():
		if len(pairs) > 1:
			pos1 = pairs[0]
			pos2 = pairs[1]
			graph.add_edge(pos1,pos2)
	return graph, start, end

def isInner(pos, width, height):
	inX = pos.x > 3 and pos.x < width-3 
	inY = pos.y > 3 and pos.y < height-3 
	return inX and inY

#Given a list of letters and a position where there is a letter thas is connected to a walkable space
#Returns the joined letters and position
def findPortalName(pos, letterPositions):
	firstLetter = letterPositions[pos]
	up = pos.add(Vector2.up)
	left = pos.add(Vector2.left)
	down = pos.add(Vector2.down)
	right = pos.add(Vector2.right)
	if up in letterPositions:
		return letterPositions[up]+firstLetter
	if left in letterPositions:
		return letterPositions[left]+firstLetter
	if right in letterPositions:
		return firstLetter+letterPositions[right]
	if down in letterPositions:
		return firstLetter+letterPositions[down]
	raise Exception('Bad coder is bad')

#Problem code

def part1(graph, start, end):
	#print(nx.shortest_path(graph, start, end))
	return nx.shortest_path_length(graph, start, end)

def part2(graph, start, end):
	#print(nx.shortest_path(graph, start, end))
	#maxDepth = 0
	#path = nx.shortest_path(graph, start, end)
	#for vec in path:
	#	maxDepth = max(vec.z, maxDepth)
	#print(maxDepth)
	return nx.shortest_path_length(graph, start, end)

#Execution stuff

def test1():
	rawInput = "         A           \n         A           \n  #######.#########  \n  #######.........#  \n  #######.#######.#  \n  #######.#######.#  \n  #######.#######.#  \n  #####  B    ###.#  \nBC...##  C    ###.#  \n  ##.##       ###.#  \n  ##...DE  F  ###.#  \n  #####    G  ###.#  \n  #########.#####.#  \nDE..#######...###.#  \n  #.#########.###.#  \nFG..#########.....#  \n  ###########.#####  \n             Z       \n             Z       "
	graph, start, end = dataToGraph(rawInput)
	print(part1(graph, start, end))
	return

def test2():
	rawInput = "             Z L X W       C                 \n             Z P Q B       K                 \n  ###########.#.#.#.#######.###############  \n  #...#.......#.#.......#.#.......#.#.#...#  \n  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  \n  #.#...#.#.#...#.#.#...#...#...#.#.......#  \n  #.###.#######.###.###.#.###.###.#.#######  \n  #...#.......#.#...#...#.............#...#  \n  #.#########.#######.#.#######.#######.###  \n  #...#.#    F       R I       Z    #.#.#.#  \n  #.###.#    D       E C       H    #.#.#.#  \n  #.#...#                           #...#.#  \n  #.###.#                           #.###.#  \n  #.#....OA                       WB..#.#..ZH\n  #.###.#                           #.#.#.#  \nCJ......#                           #.....#  \n  #######                           #######  \n  #.#....CK                         #......IC\n  #.###.#                           #.###.#  \n  #.....#                           #...#.#  \n  ###.###                           #.#.#.#  \nXF....#.#                         RF..#.#.#  \n  #####.#                           #######  \n  #......CJ                       NM..#...#  \n  ###.#.#                           #.###.#  \nRE....#.#                           #......RF\n  ###.###        X   X       L      #.#.#.#  \n  #.....#        F   Q       P      #.#.#.#  \n  ###.###########.###.#######.#########.###  \n  #.....#...#.....#.......#...#.....#.#...#  \n  #####.#.###.#######.#######.###.###.#.#.#  \n  #.......#.......#.#.#.#.#...#...#...#.#.#  \n  #####.###.#####.#.#.#.#.###.###.#.###.###  \n  #.......#.....#.#...#...............#...#  \n  #############.#.#.###.###################  \n               A O F   N                     \n               A A D   M                     "
	graph, start, end = dataTo3DGraph(rawInput)
	print(part2(graph, start, end))
	return

def main():
	rawInput = open("./input/20.txt").read()
	graph, start, end = dataToGraph(rawInput)
	print(part1(graph, start, end))
	graph, start, end = dataTo3DGraph(rawInput)
	print(part2(graph, start, end))
	return

#test1()
#test2()
main()