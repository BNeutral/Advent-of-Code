#Problem code

def part1(amountOfRecipes):
	scoreBoard = [3,7]
	elves = [ Elf(0, scoreBoard), Elf(1,scoreBoard)]
	while len(scoreBoard) < amountOfRecipes+10:
		makeRecipe(elves, scoreBoard)
		for elf in elves:
			elf.advance()
	return findFinalScore(scoreBoard, amountOfRecipes, 10)

def makeRecipe(elves, scoreBoard):
	sum = 0
	for elf in elves:
		sum += scoreBoard[elf.index]
	if sum < 10:
		scoreBoard.append(sum)
	else:
		scoreBoard.append(sum//10)
		scoreBoard.append(sum%10)

def findFinalScore(scoreBoard, index, count):
	sum = ""
	for x in range(index,index+count):
		sum += str(scoreBoard[x])
	return sum

def part2(scoreToFind):
	scoreBoard = [3,7]
	elves = [ Elf(0, scoreBoard), Elf(1,scoreBoard)]
	x = 0
	scoreLength = len(scoreToFind)
	while True:
		x += 1
		makeRecipe(elves, scoreBoard)
		for elf in elves:
			elf.advance()
		for elfCount in range(len(elves)):
			index = len(scoreBoard)-scoreLength-elfCount
			result = findFinalScore(scoreBoard, index, scoreLength)
			if result == scoreToFind:
				return index

class Elf:

	classVar = 1

	def __init__(self, currentIndex, scoreBoard):
		self.index = currentIndex
		self.scoreBoard = scoreBoard

	def advance(self):
		self.index += self.scoreBoard[self.index]+1
		self.index %= len(self.scoreBoard)

#Execution stuff

def test1():
	print(part1(9))
	print(part1(5))
	print(part1(18))
	print(part1(2018))
	return

def test2():
	print(part2("51589"))
	print(part2("01245"))
	print(part2("92510"))
	print(part2("59414"))
	return

def main():
	#print(part1(323081))
	print(part2("323081"))
	return

#test1()
#test2()
main()
