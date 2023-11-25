--- Reads a file and performs some parsing
---@param fileName string Filename relative to running folder
---@param parseFunc function(string)
---@return table
function ReadAndParse(fileName, parseFunc)
    local lines = {}
    local counter = 1
    for line in io.lines(fileName) do
        table.insert(lines, counter, parseFunc(line))
        counter = counter + 1
    end    
    return lines
end