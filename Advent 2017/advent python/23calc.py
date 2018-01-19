import math

def divisorGenerator(n):
    large_divisors = []
    for i in xrange(1, int(math.sqrt(n) + 1)):
        if n % i == 0:
            yield i
            if i*i != n:
                large_divisors.append(n / i)
    for divisor in reversed(large_divisors):
        yield divisor

count = 0
e = 2
d = 2
op = False
for b in range(107900,124901,17):
	div = list(divisorGenerator(b))
	div.remove(1)
	for d in div :
		for e in div:
			if (e*d) == b:
				op = True
	if op:
		count+=1
		op = False
	
print count
