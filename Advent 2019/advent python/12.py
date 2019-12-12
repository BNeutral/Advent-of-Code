from collections import defaultdict
from util import *
import re
import math

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

def part1(positions, steps):
	moons = simulateMoons(positions,steps)
	total = 0
	for moon in moons:
		potential = 0
		kinetic = 0
		for i in range(3):
			potential += abs(moon.pos[i])
			kinetic += abs(moon.velocity[i])
		total += potential*kinetic
	return total

def part2(positions):
	return simulateMoonUntilRepeat(positions, 2000000, 5)

def simulateMoons(positions,steps):
	moons, moonPairs = createMoonsAndPairs(positions)
	for _ in range(steps):
		updateMoons(moons, moonPairs)
	return moons

def simulateMoonUntilRepeat(positions, steps, repetitionDegree):
	moons, moonPairs = createMoonsAndPairs(positions)
	stateLength = len(moons)*6
	initialState = []
	for moon in moons:
		initialState.extend(list(moon.pos))
		initialState.extend(list(moon.velocity))
	stepCounter = 0
	sightings = []
	cycles = []
	for _ in range(stateLength):
		sightings.append(set())
		cycles.append([])
	for _ in range(steps):
		updateMoons(moons, moonPairs)
		stepCounter += 1
		state = []
		for moon in moons:
			state.extend(list(moon.pos))
			state.extend(list(moon.velocity))
		for i in range(stateLength):
			if state[i] == initialState[i]:
				sightings[i].add(stepCounter)
				cycleLength = stepCounter//repetitionDegree
				hasRepeated = True
				for x in range(repetitionDegree):
					if not cycleLength*(x+1) in sightings[i]:
						hasRepeated = False
						break
				if hasRepeated:
					cycles[i].append(cycleLength)		
	smallestPeriods = []
	for i in range(stateLength):
		smallestPeriods.append(min(cycles[i]))
	smallestPeriods = list(dict.fromkeys(smallestPeriods))
	return smallestPeriods,minimumCommonMultiple(smallestPeriods)

def createMoonsAndPairs(positions):
	moons = []
	for pos in positions:
		moons.append(Moon(pos))
	moonPairs = []
	for x in range(len(moons)):
		for y in range(x+1,len(moons)):
			moonPairs.append((moons[x],moons[y]))
	return moons, moonPairs

def updateMoons(moons, moonPairs):
	for pair in moonPairs:
		pair[0].updateVelocity(pair[1]) 
	for moon in moons:
		moon.updatePosition()

class Moon:

	def __init__(self, position):
		self.pos = position
		self.velocity = Vector3(0,0,0)

	def updateVelocity(self, otherMoon, simulationSpeed=1):
		for i in range(3):
			if self.pos[i] < otherMoon.pos[i]:
				self.velocity[i] += 1 * simulationSpeed
				otherMoon.velocity[i] -= 1 * simulationSpeed
			elif self.pos[i] > otherMoon.pos[i]:
				self.velocity[i] -= 1 * simulationSpeed
				otherMoon.velocity[i] += 1 * simulationSpeed

	def updatePosition(self):
		self.pos = self.pos.add(self.velocity)

#Execution stuff

def test1():
	positions = [Vector3(-1,0,2),Vector3(2,-10,-7),Vector3(4,-8,8),Vector3(3,5,-1)]
	print(part1(positions,10))

def test2():
	positions = [Vector3(-1,0,2),Vector3(2,-10,-7),Vector3(4,-8,8),Vector3(3,5,-1)]
	print(part2(positions))
	positions = [Vector3(-8,-10,0),Vector3(5,5,10),Vector3(2,-7,3),Vector3(9,-8,-3)]
	print(part2(positions))

def main():
	print("Pypy usage is recommended for this problem. Convergence criteria is vague, tweak arguments for part 2 if needed.")
	positions = [Vector3(7,10,17),Vector3(-2,7,0),Vector3(12,5,12),Vector3(5,-8,6)]
	print(part1(positions,1000))
	print(part2(positions))
	return

#test1()
test2()
main()