import re
import copy

#File parsing stuff
def dataToParsedArray(stringData) :
	units = []
	side = 0
	for line in stringData.split("\n"):
		line = line.strip()
		if "Immune System:" in line:
			side = 0
		elif "Infection:" in line:
			side = 1
		elif line != "":
			units.append(UnitGroup(line, side))
	return units

#Problem code

def part1(units, boost = 0):
	oldAliveUnits = -1
	aliveUnits = 0
	for unit in units:
		if unit.side == 0:
			unit.attackDamage += boost
	sidesAlive = [0,0]
	for unit in units:
		sidesAlive[unit.side] += 1
	while 0 not in sidesAlive:
		units.sort(key=lambda x: (x.effectivePower(), x.initiative), reverse=True)
		possibleTargets = set(units)
		targets = {}
		for unit in units:
			target = unit.selectTarget(possibleTargets)
			targets[unit] = target
			if target:
				possibleTargets.remove(target)	
		units.sort(key=lambda u: u.initiative,reverse=True)
		i = 0
		while i < len(units):
			unit = units[i]
			target = targets[unit]
			if target:
				unit.dealDamage(target)
				if target.units <= 0:
					tgIndex = units.index(target)
					units.remove(target)
					sidesAlive[target.side] -= 1
					if tgIndex < i:
						i -= 1					
			i += 1
		aliveUnits = sum(unit.units for unit in units)
		if oldAliveUnits == aliveUnits:
			return -1,-1
		oldAliveUnits = aliveUnits
	return aliveUnits, units[0].side


def part2(units):
	boost = 0
	winningSide = 1
	alive = 0
	while winningSide != 0:
		unitCopy = copy.deepcopy(units)
		boost += 1
		alive, winningSide = part1(unitCopy, boost)
		print boost
	return alive, boost

class UnitGroup:

	regex = re.compile(r'^(\d+) units each with (\d+) hit points.* with an attack that does (\d+) (\w+) damage at initiative (\d+)$')
	regexWeak = re.compile(r'.*weak to ([\w, ]+)[;)]')
	regexImmune = re.compile(r'.*immune to ([\w, ]+)[;)]')

	def __init__(self, string, side):
		match = UnitGroup.regex.match(string)
		self.units = int(match.group(1))
		self.hitPoints = int(match.group(2))
		self.attackDamage = int(match.group(3))
		self.attacktype = match.group(4)
		self.initiative = int(match.group(5))
		self.weakness = set()
		self.immunities = set()
		weakness = UnitGroup.regexWeak.match(string)
		immunities = UnitGroup.regexImmune.match(string)
		if weakness:			
			self.weakness = set( weakness.group(1).replace(" ","").split(",") )
		if immunities:
			self.immunities = set( immunities.group(1).replace(" ","").split(",") )
		self.side = side

	def effectivePower(self):
		return self.attackDamage * self.units

	def possibleDamage(self, other):
		if self.attacktype in other.weakness:
			return self.effectivePower()*2
		elif self.attacktype in other.immunities:
			return 0
		else:
			return self.effectivePower()

	def selectTarget(self, possibleTargets):
		selectedTarget = None
		maxDamage = 0
		maxEfP = 0
		for target in possibleTargets:
			if self.side != target.side:
				possibleDamage = self.possibleDamage(target)
				targetEfP = target.effectivePower()
				if possibleDamage == 0:
					continue
				elif possibleDamage > maxDamage or (possibleDamage == maxDamage and maxEfP < targetEfP):
					maxDamage = possibleDamage
					maxEfP = targetEfP
					selectedTarget = target
		return selectedTarget

	def dealDamage(self, target):
		damage = self.possibleDamage(target)
		target.units -= damage//target.hitPoints	

	def __repr__(self):
		return str(self.__dict__)

	def __hash__(self):
		return id(self)

#Execution stuff

def test1():
	rawInput = "Immune System:\n17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2\n989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3\nInfection:\n801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1\n4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4"
	data = dataToParsedArray(rawInput)
	print(part1(data))
	return

def test2():
	rawInput = "Immune System:\n17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2\n989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3\nInfection:\n801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1\n4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4"
	data = dataToParsedArray(rawInput)
	print(part1(data,1570))
	return

def test3():
	rawInput = "Immune System:\n17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2\n989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3\nInfection:\n801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1\n4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4"
	data = dataToParsedArray(rawInput)
	print(part2(data))
	return

def main():
	rawInput = open("./input/24.txt","r").read()
	data = dataToParsedArray(rawInput)
	#print(part1(data))
	print(part2(data))
	return

#test1()
#test2()
#test3()
main()
