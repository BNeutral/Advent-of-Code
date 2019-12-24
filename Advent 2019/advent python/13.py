from util import *
from intcode import Interpreter

#Problem code

def part1(data):
	program = Interpreter(data, [], False)
	program.runProgram()
	_,info = getOutputAsDict(program)
	return info["blocks"]

def part2(data):
	data = data.copy()
	data[0] = 2
	program = Interpreter(data, [], False)
	thread = program.runInThread()
	screen = {}
	info = {}
	while True:
		if program.awaitingInput or not program.isRunning:
			newScreen,newInfo = getOutputAsDict(program)
			for key,value in newScreen.items():
				screen[key] = value
			for key,value in newInfo.items():
				info[key] = value
			#printScreen(screen)
			if not program.isRunning:
				thread.join()
				return info["score"]
			paddleX = info["paddle"].x
			ballX = info["ball"].x
			if ballX < paddleX:
				program.giveInput(-1)
			elif ballX > paddleX:
				program.giveInput(1)
			else:
				program.giveInput(0)

def printScreen(dicOutput):
	text = drawDictScreen(dicOutput, [" ","▓","░","=","*"])
	if "score" in dicOutput.keys():
		scoreText = "Score:"+dicOutput["score"]
		text += scoreText
	print(text)

def countBlocks(dicOutput):
	blocks = 0
	for value in dicOutput.values():
		if value == 2:
			blocks += 1
	return blocks

def getOutputAsDict(interpreter):
	dic = {}
	info = {}
	info["blocks"] = 0
	while not interpreter.output.empty() > 0:
		x,y,tile = getOutput(interpreter)
		if tile == 2:
			info["blocks"] += 1
		elif tile == 3:
			info["paddle"] = Vector2(x,y)
		elif tile == 4:
			info["ball"] = Vector2(x,y)
		if x == -1 and y == 0:
			info["score"] = tile
		else:
			dic[Vector2(x,y)] = tile
	return dic, info

def getOutput(interpreter):
	x = interpreter.output.get()
	y = interpreter.output.get()
	tileType = interpreter.output.get()
	return x,y,tileType

#Execution stuff

def main():
	rawInput = open("./input/13.txt").read()
	data = commaSeparatedLineToInts(rawInput)
	print("Computing. Uncomment line 30 if you want visual updates...")
	print(part1(data))
	print(part2(data))
	return

#test1()
#test2()
main()