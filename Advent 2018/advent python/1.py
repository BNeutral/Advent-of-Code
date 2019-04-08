#File parsing stuff
def dataToParsedArray(stringData) :
	result = [] 
	for line in stringData.split("\n"):
		line = line.strip()
		if line != "":
			result.append(parse(line))
	return result

def parse(line) :
	return int(line)

#Problem code
def part1(data):
	return sum(data)


def part2(data, sum, set):
	for num in data:
		sum += num
		if (sum in set):
			return sum
		set.add(sum)
	return part2(data, sum, set)

#Execution stuff
def test1():
	data = [+1, +1, +1]
	print(part1(data))
	return

def test2():
	data = [+3, +3, +4, -2, -4]
	print(part2(data, 0, set()))
	return

def main():
	rawInput = open("./input/1.txt").read()
	data = dataToParsedArray(rawInput)
	print(part1(data))
	print(part2(data, 0, set()))
	return

main()
