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
	fuel = 0
	for mass in data:
		fuel += findFuel(mass)
	return fuel

def part2(data):
	total = 0
	for mass in data:
		while mass > 0:
			fuel = findFuel(mass)
			if fuel <= 0:
				break
			total += fuel
			mass = fuel
	return total

def findFuel(x):
	return (x//3 - 2)

def main():
	rawInput = open("./input/1.txt").read()
	data = dataToParsedArray(rawInput)
	print(part1(data))
	print(part2(data))
	return

#test1()
#test2()
main()

#Python reminders
#range(start, end+1, step), len
#{}, for k in dict, for k,v in dict.items(), for v in dict.values()  
#set(), .add(x), .remove(x), .discard(x) no error if missing, x in s, |= union, &= intersect, -= difference, .copy()
#[], .append(), .insert(i,x), .pop([i]), .remove(x), .reverse(), sort(arr) in place, sorted(arr) new arr 
#map(single param function, list)
#filter(single param boolean returning function, list)
#reduce(2 param function, list)
#lambda x: x**2
#// integer division in python3