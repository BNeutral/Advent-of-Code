require("fileReading")
require("util")

local Assignments = { start = 0, finish = 0 }

function Assignments:new(obj)
    obj = obj or {}
    self.__index = self
    return setmetatable(obj, self)
end

function Assignments:newFromString(input)
    local obj = Assignments:new()
    local split = SplitString(input, "-")
    obj.start = tonumber(split[1])
    obj.finish = tonumber(split[2])
    return obj
end

function Assignments:contains(otherAssignment)
    return self.start <= otherAssignment.start and otherAssignment.finish <= self.finish
end

function Assignments:overlaps(otherAssignment)
    return self.start <= otherAssignment.finish and self.finish >= otherAssignment.start 
end

local AssignmentPair = { first = {}, second = {} }

function AssignmentPair:new(obj)
    obj = obj or {}
    self.__index = self
    setmetatable(obj, self)
    return obj
end

function AssignmentPair:newFromString(input)
    local obj = AssignmentPair:new()
    local split = SplitString(input,",")
    obj.first = Assignments:newFromString(split[1])
    obj.second = Assignments:newFromString(split[2])
    return obj
end

function AssignmentPair:oneContainsOther()
    return self.first:contains(self.second) or self.second:contains(self.first)
end

function AssignmentPair:oneOverlapsOther()
    return self.first:overlaps(self.second) or self.second:overlaps(self.first)
end

local function ParseInputLine(input)
    return AssignmentPair:newFromString(input)
end

local function SolvePart1(data)
    local total = 0
    for key, value in pairs(data) do
        if value:oneContainsOther() then
            total = total + 1
        end
    end
    return total
end

local function SolvePart2(data)
    local total = 0
    for key, value in pairs(data) do
        if value:oneOverlapsOther() then
            total = total + 1
        end
    end
    return total
end

function Solve4(isTest)
    local path = "./inputs/4.txt"
    if isTest then
        path = "./testInputs/4.txt"
    end
    local data = ReadAndParse(path, ParseInputLine)

    return SolvePart1(data) .. " - " .. SolvePart2(data)
end