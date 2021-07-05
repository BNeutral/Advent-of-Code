from collections import defaultdict
from util import *
import re

#File parsing stuff
def dataToParsedArray(stringData) :
	result = [] 
	concatLine = "" 
	for line in stringData.split("\n"):
		line = line.strip()
		if line != "":
			if concatLine != "":
				concatLine += " "
			concatLine += line
		else:
			result.append(parse(concatLine))
			concatLine = ""
	if concatLine != "":
		result.append(parse(concatLine))
	return result

def parse(line) :
	return line

#Problem code

def part(data, validate):
	passports = []
	for entry in data:
		passports.append(Passport(entry, validate))
	count = 0
	for passport in passports:
		try:
			if passport.isValid():
				count += 1
		except AttributeError:
			pass
	return count

class Passport:

	def validateByr(self, string):
		val = int(string)
		return val >= 1920 and val <= 2002

	def validateIyr(self, string):
		val = int(string)
		return val >= 2010 and val <= 2020

	def validateEyr(self, string):
		val = int(string)
		return val >= 2020 and val <= 2030

	def validateHgt(self, string):
		lastChars = string[-2:]
		toVal = string[0:-2]
		if toVal == "":
			return False
		val = int(toVal)
		if lastChars == "cm":
			return val >= 150 and val <= 193
		if lastChars == "in":
			return val >= 59 and val <= 76
		return False

	def validateHcl(self, string):
		regex = re.compile(r'^#[0-9a-f]{6}$')
		match = regex.match(string)
		return match != None

	def validateEcl(self, string):
		return string == "amb" or string == "blu" or string == "brn" or string == "gry" or string == "grn" or string == "hzl" or string == "oth"

	def validatePid(self, string):
		regex = re.compile(r'^[0-9]{9}$')
		match = regex.match(string)
		return match != None

	def validateCid(self, string):
		return True

	matchings = { "byr" : validateByr, "iyr" : validateIyr, "eyr" : validateEyr, "hgt" : validateHgt, "hcl" : validateHcl, "ecl" : validateEcl, "pid" : validatePid, "cid" : validateCid }

	def __init__(self, string, validate):
		split = string.split(" ")
		for entry in split:
			subsplit = entry.split(":")
			if subsplit[0] in Passport.matchings:
				if validate:
					if not Passport.matchings[subsplit[0]](self,subsplit[1]):
						#print("invalid"+entry)
						continue
				setattr(self, subsplit[0], subsplit[1])

	def isValid(self):
		return self.byr != None and self.iyr != None and self.eyr != None and self.hgt != None and self.hcl != None and self.ecl != None and self.pid != None 

#Execution stuff

def test1():
	rawInput = "ecl:gry pid:860033327 eyr:2020 hcl:#fffffd\nbyr:1937 iyr:2017 cid:147 hgt:183cm\n\niyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884\nhcl:#cfa07d byr:1929\n\nhcl:#ae17e1 iyr:2013\neyr:2024\necl:brn pid:760753108 byr:1931\nhgt:179cm\n\nhcl:#cfa07d eyr:2025 pid:166559648\niyr:2011 ecl:brn hgt:59in\n"
	data = dataToParsedArray(rawInput)
	print(part(data, False))
	return

def test2():
	input1 = "eyr:1972 cid:100\nhcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926\n\niyr:2019\nhcl:#602927 eyr:1967 hgt:170cm\necl:grn pid:012533040 byr:1946\n\nhcl:dab227 iyr:2012\necl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277\n\nhgt:59cm ecl:zzz\neyr:2038 hcl:74454a iyr:2023\npid:3556412378 byr:2007"
	data = dataToParsedArray(input1)
	print(part(data, True))
	input2 = "pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980\nhcl:#623a2f\n\neyr:2029 ecl:blu cid:129 byr:1989\niyr:2014 pid:896056539 hcl:#a97842 hgt:165cm\n\nhcl:#888785\nhgt:164cm byr:2001 iyr:2015 cid:88\npid:545766238 ecl:hzl\neyr:2022\n\niyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719\n"
	data = dataToParsedArray(input2)
	print(part(data, True))
	return

def main():
	rawInput = open("./input/4.txt").read()
	data = dataToParsedArray(rawInput)
	print(part(data, False))
	print(part(data, True))
	return

#test1()
#test2()
main()