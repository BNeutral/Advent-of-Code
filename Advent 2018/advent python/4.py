import re
from datetime import datetime,timedelta
from collections import defaultdict

#File parsing stuff
def dataToParsedArray(stringData) :
	result = [] 
	for line in stringData.split("\n"):
		line = line.strip()
		if line != "":
			result.append(parse(line))
	return result

def parse(line) :
	return Entry(line)

#Problem code

def convert(data):
	currentGuard = 0
	guardsCumulativeSleep = defaultdict(int)
	guardsMinutesAsleep = defaultdict(lambda: [0 for _ in range(60)])
	regex = re.compile(r'^.*#(\d+).*$')
	timeFellAsleep = datetime.now()
	for entry in data:
		if "begins" in entry.action:
			match = regex.match(entry.action)
			currentGuard = int(match.group(1))
		elif "wakes" in entry.action:
			minutesAsleep = (entry.date - timeFellAsleep).seconds/60
			guardsCumulativeSleep[currentGuard] += minutesAsleep	
			for x in range(timeFellAsleep.minute, timeFellAsleep.minute + minutesAsleep):
				guardsMinutesAsleep[currentGuard][x] += 1				
		elif "asleep" in entry.action:
			timeFellAsleep = entry.date
	return guardsCumulativeSleep, guardsMinutesAsleep

def part1(data):
	guardsCumulativeSleep, guardsMinutesAsleep = convert(data)
	guard = 0
	sleepTotal = 0
	for key in guardsCumulativeSleep:
		if guardsCumulativeSleep[key] > sleepTotal:
			sleepTotal = guardsCumulativeSleep[key]
			guard = key
	bestMinute = 0
	maxMinute = 0
	for minute in range(0,60):
		if guardsMinutesAsleep[guard][minute] > maxMinute:
			maxMinute = guardsMinutesAsleep[guard][minute]
			bestMinute = minute
	return guard*bestMinute

def part2(data):
	_, guardsMinutesAsleep = convert(data)
	bestGuard = 0
	bestMinute = 0
	maxRepeats = 0
	for guard in guardsMinutesAsleep:
		for minute in range(0,60):
			if guardsMinutesAsleep[guard][minute] > maxRepeats:
				maxRepeats = guardsMinutesAsleep[guard][minute]
				bestMinute = minute
				bestGuard = guard
	return bestGuard*bestMinute

class Entry:

	def __init__(self, string):
		regex = re.compile(r'^\[(.*)\] (.*)$')
		match = regex.match(string)
		self.date = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M')
		self.action = match.group(2)

	def __repr__(self):
		return '{} {}'.format(self.date,self.action)

	def __cmp__(self,other):
		return cmp(self.date,other.date)

#Execution stuff

def test1():
	data = "[1518-11-01 00:00] Guard #10 begins shift"
	print(Entry(data))
	return

def test2():
	inp = "[1518-11-01 00:00] Guard #10 begins shift\n[1518-11-01 00:05] falls asleep\n[1518-11-01 00:25] wakes up\n[1518-11-01 00:30] falls asleep\n[1518-11-01 00:55] wakes up\n[1518-11-01 23:58] Guard #99 begins shift\n[1518-11-02 00:40] falls asleep\n[1518-11-02 00:50] wakes up\n[1518-11-03 00:05] Guard #10 begins shift\n[1518-11-03 00:24] falls asleep\n[1518-11-03 00:29] wakes up\n[1518-11-04 00:02] Guard #99 begins shift\n[1518-11-04 00:36] falls asleep\n[1518-11-04 00:46] wakes up\n[1518-11-05 00:03] Guard #99 begins shift\n[1518-11-05 00:45] falls asleep\n[1518-11-05 00:55] wakes up"
	data = dataToParsedArray(inp)
	print(part1(data))
	print(part2(data))
	return

def main():
	rawInput = open("./input/4.txt").read()
	data = dataToParsedArray(rawInput)
	data.sort()
	print(part1(data))
	print(part2(data))
	return

main()
