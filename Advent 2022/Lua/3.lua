require("fileReading")
require("util")

local letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
local Mapping = {} 
for i = 1, #letters, 1 do
    Mapping[letters:sub(i, i)] = i
end

local function toSet(string)
    local set = {}
    for i = 1, #string do
        local c = string:sub(i, i)
        set[c] = true
    end
    return set
end

local function setIntersect(...)
    local result = {}
    for key, value in pairs(arg[1]) do
        result[key] = true
    end

    for key, _ in pairs(arg[1]) do
        for _, value in ipairs(arg) do
            if value[key] == nil then
                result[key] = nil
                break
            end
        end
    end
    
    return result
end

local Sack = {first = {}, second = {}}

function Sack:new(obj)
    obj = obj or {}
    setmetatable(obj, self)
    self.__index = self
    return obj
end

function Sack:parse(input)
    self.first = toSet(string.sub(input, 0, #input / 2))
    self.second = toSet(string.sub(input, #input / 2 + 1, #input))
end

function Sack:findRepeat()
    local result = setIntersect(self.first, self.second)
    return next(result)
end

local function ParseToSacks(input)
    local result = Sack:new()
    result:parse(input)
    return result
end

local function SolvePart1(data)
    local total = 0
    for key, value in pairs(data) do
        local rep = value:findRepeat()
        total = total + Mapping[rep]
    end
    return total
end

local function ParseToSets(input)
    return toSet(input)
end

local function SolvePart2(data)
    local total = 0
    for i = 1, #data, 3 do
        local result = setIntersect(data[i],data[i+1],data[i+2])
        total = total + Mapping[next(result)]
    end
    return total
end

function Solve3(isTest)
    local path = "./inputs/3.txt"
    if isTest then
        path = "./testInputs/3.txt"
    end

    return SolvePart1(ReadAndParse(path, ParseToSacks)) .. " - " .. SolvePart2(ReadAndParse(path, ParseToSets))
end