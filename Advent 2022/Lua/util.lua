---Checks if a string is only whitespace
---@param str string string to check for whitespace
---@return boolean
function IsWhitespace(str)
    return str:match("%s") ~= nil
end

---comment sets a table to return a default value
---@param table table
---@param defaultValue any default value
function SetDefault(table, defaultValue)
    local metaTable = { __index = function() return defaultValue end }
    setmetatable(table, metaTable)
end

---comment Reduce table funciton. Given a table and initial value, applies to all elements and accumulates
---@param table table 
---@param initialValue any
---@param reduce function(any, tableelement)
function Fold(table, initialValue, reduce)
    for _, value in ipairs(table) do
        initialValue = reduce(initialValue, value)
    end
    return initialValue
end

---comment Split a string
---@param input_str any
---@param separator any
---@return table
function SplitString(input_str, separator)
    local substrings = {}
    for substring in input_str:gmatch("[^" .. separator .. "]+") do
        table.insert(substrings, substring)
    end
    return substrings
end