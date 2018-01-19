class MatrixBase:
	def __init__(self, string):
		split = string.split("/")
		self.contents = split
		return		

	def rotateL(self):
		size = self.size()
		tmpCont = []
		result = []
		for y in self.contents:
			tmpCont.append(list(y))
			result.append(list(y))

		for y in range(0,size):
			for x in range(0,size):
				result[y][x] = tmpCont[x][size-1-y]

		self.contents = []
		for y in result:
			self.contents.append(''.join(y))
		return

	def flipH(self):
		size = self.size();
		for y in range(0,size):
			self.contents[y] = self.contents[y][::-1]

	def subMatrix(self, size, offsetX, offsetY) :
		result = []
		strSult = ""
		for y in range(offsetY,offsetY+size) :
			result.append(self.contents[y][offsetX:offsetX+size])
		for x in result:	
			strSult += x
			strSult += "/"
		strSult = strSult.rstrip("/")
		return MatrixBase(str(strSult))
			

	def size(self):
		return len(self.contents[0])

	def __str__(self):
		result = ""
		for x in self.contents:
			result += x+"/"
		result = result.rstrip("/")
		return result

	def nicePrint(self):
		for x in self.contents:
			print(x)

	def on(self):
		counter = 0
		for x in self.contents:
			for c in x:
				if c=="#":
					counter += 1
		return counter

	def enhance(self, rules, iterations) :
		print("start")
		for it in range (0,iterations):
			size = self.size()
			step = 3
			if size % 2 == 0:
				step = 2
			result = []
			for y in range(0,size, step):
				submatrices = []
				for x in range(0,size, step):
					subm = self.subMatrix(step, x, y)
					asText = str(subm)
					subm = rules[asText]
					submatrices.append(MatrixBase(subm))
				tam = submatrices[0].size()
				for a in range(0,tam): #per col
					row = []
					for b in submatrices: #per submatrix
						for c in range(0,tam): #per file
							row.append(b.contents[a][c])			
					result.append(''.join(row))
			resStr = ""		
			for x in result:
				resStr = resStr+x+"/"
			resStr = resStr.rstrip("/")
			self.contents = MatrixBase(resStr).contents
			print("iter "+str(it))
			print("on"+str(self.on()))

def getData() :
	f = open("./input/input21","r")
	dic = parseToDict(f)
	f.close()
	return dic

def parseToDict(iterable):
	dic = {}
	for line in iterable:
		sep = line.split("=>")
		key = sep[0].rstrip()
		rule = sep[1].strip()
		dic[key] = rule
		mat = MatrixBase(key)
		for y in range(0,2):
			mat.flipH()
			for x in range(0,4):
				mat.rotateL();
				key = str(mat)
				dic[key] = rule
	return dic

def main() :
	initial = MatrixBase(".#./..#/###")
	rules = getData()	
	initial.enhance(rules,18)

def test():
	initial = MatrixBase(".#./..#/###")
	rules = parseToDict(["../.# => ##./#../...",".#./..#/### => #..#/..../..../#..#"])	
	initial.enhance(rules,2)

def test2():
	initial = MatrixBase("...#/##.#/#..#/.#..")
	initial.nicePrint()
	print(initial.subMatrix(2,2,0))
	
main()
