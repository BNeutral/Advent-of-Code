module Day2 where

import Data.List

-- Tests

sample = "forward 5\ndown 5\nforward 8\nup 3\ndown 8\nforward 2"
test1 = part1 (lines sample)
test2 = part2 (lines sample)

-- Part 1

part1 :: [String] -> Integer
part1 input = 
    pos * depth
    where (pos,depth) = foldl parseLine (0,0) input

parseLine :: (Integer,Integer) -> String -> (Integer,Integer)
parseLine (pos,depth) ('f' : 'o' : 'r' : 'w' : 'a' : 'r' : 'd' : value) =
    (pos + read value, depth)
parseLine (pos,depth) ('u' : 'p' : value)  =
    (pos, depth - read value)
parseLine (pos,depth) ('d' : 'o' : 'w' : 'n' : value) =
    (pos, depth + read value)
parseLine (pos,depth) badInput =
    error "Bad parsing"

-- Part 2

part2 :: [String] -> Integer
part2 input = 
    pos * depth
    where (pos, depth, aim) = foldl parseLine2 (0,0,0) input

parseLine2 :: (Integer,Integer,Integer) -> String -> (Integer,Integer,Integer)
parseLine2 (pos, depth, aim) ('f' : 'o' : 'r' : 'w' : 'a' : 'r' : 'd' : value) =
    (pos + rVal, depth + rVal * aim, aim)
    where rVal = read value
parseLine2 (pos, depth, aim) ('u' : 'p' : value)  =
    (pos, depth, aim - read value)
parseLine2 (pos, depth, aim) ('d' : 'o' : 'w' : 'n' : value) =
    (pos, depth, aim + read value)
parseLine2 (pos, depth, aim) badInput =
    error "Bad parsing"

-- Main

day2 = do
    contents <- fmap lines (readFile "../input/2.txt")
    print $ ("Test1: " ++) $ show test1 
    print $ ("Test2: " ++) $ show test2   
    print $ ("Part1: " ++) $ show $ part1 contents
    print $ ("Part2: " ++) $ show $ part2 contents 
