require("1")
require("2")
require("3")
require("4")

local overrideProblem = 4
local runOnTestData = false
local maxProblem = 4

local solvers = {Solve1, Solve2, Solve3, Solve4}

-- Main function, call the command with an int arg if you want to run a specific problem instead of all of them
local function main()
    local selectedProblem = 0
    if #arg > 1 then
        selectedProblem = tonumber(arg[1])
    else
        selectedProblem = overrideProblem
    end
    if selectedProblem ~= 0 and selectedProblem > 0 and selectedProblem <= maxProblem then
        print("Solution to problem " .. selectedProblem .. ": " .. solvers[selectedProblem](runOnTestData))
    else
        for i=1,maxProblem do
            print("Solution to problem " .. i .. ": " .. solvers[i](runOnTestData))
        end
    end
end

main()