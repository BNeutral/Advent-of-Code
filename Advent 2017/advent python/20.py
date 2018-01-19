import re

class Particle:
	def __init__(self, num, x, y, z, vx, vy, vz, ax, ay, az):
		self.num = num
		self.x = int(x)
		self.y = int(y)
		self.z = int(z)
		self.vx = int(vx)
		self.vy = int(vy)
		self.vz = int(vz)
		self.ax = int(ax)
		self.ay = int(ay)
		self.az = int(az)

	def update(self):
		self.vx += self.ax;
		self.vy += self.ay;
		self.vz += self.az;
		self.x += self.vx;
		self.y += self.vy;
		self.z += self.vz;

	def collides(self, other):
		return (self.x==other.x and self.y==other.y and self.z==other.z)

def manhdistorig(p):
	return (abs(p.x)+abs(p.y)+abs(p.z))

def getData() :
	v = []
	f = open("./input/input20","r")
	num = 0
	for line in f:
		match1 = re.search(r"p=<(-?\d+),(-?\d+),(-?\d+)>", line)
		x = match1.group(1)
		y = match1.group(2)
		z = match1.group(3)
		match2 = re.search(r"v=<(-?\d+),(-?\d+),(-?\d+)>", line)
		vx = match2.group(1)
		vy = match2.group(2)
		vz = match2.group(3)
		match3 = re.search(r"a=<(-?\d+),(-?\d+),(-?\d+)>", line)
		ax = match3.group(1)
		ay = match3.group(2)
		az = match3.group(3)
		v.append(Particle(num,x,y,z,vx,vy,vz,ax,ay,az))
		num+=1
	f.close()
	return v

def main() :
	v = getData()
	c = set()
	print(v[0].vx)
	for t in range(0,50):
		for p1 in v:
			for p2 in v:
				if p1 != p2 and p1.collides(p2):
					c.add(p1)
					c.add(p2)
			p1.update()
			for p in c:
				v.remove(p)	
			c = set()		
	#v.sort(key=manhdistorig)
	print(len(v))
	
main()
