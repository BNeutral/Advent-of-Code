require("fileReading")
require("util")

local function ParseInputLine(input)

end

local function SolvePart1(data)
    return 0
end

local function SolvePart2(data)
    return 0
end

function SolveX(isTest)
    local path = "./inputs/X.txt"
    if isTest then
        path = "./testInputs/X.txt"
    end
    local data = ReadAndParse(path, ParseInputLine)

    return SolvePart1(data) .. " - " .. SolvePart2(data)
end