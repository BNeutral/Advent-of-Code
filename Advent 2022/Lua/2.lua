require("fileReading")
require("util")

local ROCK = 1
local PAPER = 2
local SCISSORS = 3

local WIN = 6
local TIE = 3
local LOSE = 0

local RPSParseMapping1 = { A = ROCK, B = PAPER, C = SCISSORS, X = ROCK, Y = PAPER, Z = SCISSORS }

local RPSMatch = {you = ROCK, other = ROCK}

function RPSMatch:new(obj)
    obj = obj or {} -- create object if user does not provide one
    setmetatable(obj, self)
    self.__index = self
    return obj
end

function RPSMatch:play()
    if self.you == self.other then
        return TIE
    end
    if self.you == ROCK then
        if self.other == SCISSORS then return WIN end
        if self.other == PAPER then return LOSE end
    end
    if self.you == PAPER then
        if self.other == ROCK then return WIN end
        if self.other == SCISSORS then return LOSE end
    end
    if self.you == SCISSORS then
        if self.other == PAPER then return WIN end
        if self.other == ROCK then return LOSE end
    end
end
function RPSMatch:part2Recalc()
    local function inner()
        if self.you == ROCK then -- Need to lose
            if self.other == ROCK then return SCISSORS end
            if self.other == PAPER then return ROCK end
            if self.other == SCISSORS then return PAPER end
        end
        if self.you == PAPER then -- Need to tie
            return self.other
        end
        if self.you == SCISSORS then -- Need to win
            if self.other == ROCK then return PAPER end
            if self.other == PAPER then return SCISSORS end
            if self.other == SCISSORS then return ROCK end
        end
    end
    self.you = inner()
end

local function ParseInputLine(input)
    local _, _, other, you = string.find(input, "(%a) (%a)")
    local result = RPSMatch:new{
        you = RPSParseMapping1[you],
        other = RPSParseMapping1[other]
    }
    return result
end

local function SolvePart1(data)
    local total = 0
    for index, value in pairs(data) do
        total = total + value.you + value:play()
    end
    return total
end

local function SolvePart2(data)
    local total = 0
    for index, value in pairs(data) do
        value:part2Recalc()
        total = total + value.you + value:play()
    end
    return total
end

function Solve2(isTest)
    local path = "./inputs/2.txt"
    if isTest then
        path = "./testInputs/2.txt"
    end
    local data = ReadAndParse(path, ParseInputLine)

    return SolvePart1(data) .. " - " .. SolvePart2(data)
end