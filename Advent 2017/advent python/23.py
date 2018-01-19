def getData() :
	f = open("./input/input23fixed","r")
	parsed = parse(f)
	f.close()
	return parsed

def parse(f):
	result = []
	for line in f:
		line = line.rstrip('\n')
		result.append(line.split(' '))
	return result

def execute(data):
	pc = 0
	registers = {}
	registers["a"] = 1
	registers["b"] = 0
	registers["c"] = 0
	registers["d"] = 0
	registers["e"] = 0
	registers["f"] = 0
	registers["g"] = 0
	registers["h"] = 0
	mult = 0
	while True:
		if (pc < 0 or pc >= len(data)) :
			return registers["h"] 
		instrucion = data[pc][0]
		x = data[pc][1]
		y = data[pc][2]
		num = 0
		if x[0].isalpha():
			xnum = registers[x] 
		else:
			xnum = int(x)
		if y[0].isalpha():
			y = registers[y] 
		else:
			y = int(y)
		if instrucion == "set":
			registers[x] = y
			pc += 1
		elif instrucion == "sub":
			registers[x] -= y
			pc += 1
		elif instrucion == "mul":
			registers[x] *= y
			mult += 1
			pc += 1
		elif instrucion == "jnz":
			if not xnum == 0:				
				pc += y
			else:
				pc += 1

def main() :
	data = getData()
	print(execute(data))



def test() :
	return 0

main()
