def jump(data) :
	pc = 0
	jmpc = 0;
	while True:
		if (pc > len(data)-1):
			return jmpc
		cur = data[pc]
		jmpc += 1;
		data[pc] += 1
		pc += cur

def jump2(data) :
	pc = 0
	jmpc = 0;
	while True:
		if (pc > len(data)-1):
			return jmpc
		cur = data[pc]
		jmpc += 1;
		if (cur >= 3) :
			data[pc] -= 1
		else :
			data[pc] += 1
		pc += cur

def getData() :
	v = []
	f = open("./input/input5","r")
	num = 0
	for line in f:
		v.append(int(line))
	f.close()
	return v

def main():
	v = getData()
	print(jump2(v))
	return

def test1():
	v = [0,3,0,1,-3]
	print(jump(v))

def test2():
	v = [0,3,0,1,-3]
	print(jump2(v))
	return

main()
