require("fileReading")
require("util")

local function ParseInputLine(input)
    if IsWhitespace(input) then
        return nil
    else
        return tonumber(input)
    end
end

local function FoldSum(accumulator, value)
    return accumulator + value    
end

local function SolvePart1(elfInventory)
    local max = 0
    for _, value in ipairs(elfInventory) do
        local sum = Fold(value, 0, FoldSum)
        if sum > max then
            max = sum
        end
    end
    return max
end

local function SolvePart2(elfInventory)
    local maxes = {}
    for _, value in ipairs(elfInventory) do
        table.insert(maxes, Fold(value, 0, FoldSum))
    end
    local function greaterThan(a, b)
        return a > b
    end
    table.sort(maxes, greaterThan)
    return maxes[1] + maxes[2] + maxes[3]
end

function Solve1(isTest)
    local path = "./inputs/1.txt"
    if isTest then
        path = "./testInputs/1.txt"
    end
    local intAndNilArray = ReadAndParse(path, ParseInputLine)
    local elfInventory = {}
    local counter = 1
    for i = 1,#intAndNilArray do
        local value = intAndNilArray[i]
        if elfInventory[counter] == nil then
            elfInventory[counter] = {}
        end
        if value == nil then
            counter = counter + 1
        else
            table.insert(elfInventory[counter], value)
        end
    end

    return SolvePart1(elfInventory) .. " - " .. SolvePart2(elfInventory)
end