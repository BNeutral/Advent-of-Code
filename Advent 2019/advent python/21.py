from util import *
from intcode import Interpreter

#Problem code

def part1(data):
	droid = SpringDroid(data)
	return droid.walk()

def part2(data):
	droid = SpringDroid(data)
	return droid.run()

class SpringDroid:

	def __init__(self, data):
		self.program = Interpreter(data, [], False)

	def walk(self):
		script = [
			"NOT A J",
			"NOT B T",
			"OR T J",
			"NOT C T",
			"OR T J",
			"AND D J"
			]
		for line in script:
			self.program.sendASCIIInput(line)
		self.program.sendASCIIInput("WALK")
		self.program.runProgram()
		#print(self.program.getASCIIOutput())	
		output = self.program.output.get()	
		while output < 256:
			output = self.program.output.get()
		return output

	def run(self):
		script = [
			"NOT A J",
			"NOT B T",
			"OR T J",
			"NOT C T",
			"OR T J",
			"AND D J",
			"AND H J",
			"NOT A T", 
			"AND D T",
			"AND E T",
			"OR T J"
			]
		for line in script:
			self.program.sendASCIIInput(line)
		self.program.sendASCIIInput("RUN")
		self.program.runProgram()
		#print(self.program.getASCIIOutput())	
		output = self.program.output.get()	
		while output < 256:
			output = self.program.output.get()
		return output

#Execution stuff

def main():
	rawInput = open("./input/21.txt").read()
	data = commaSeparatedLineToInts(rawInput)
	print(part1(data))
	print(part2(data))
	return

main()