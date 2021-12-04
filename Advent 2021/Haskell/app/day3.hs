module Day3 where

import Data.List
import Data.Char(digitToInt)

-- Tests

sample = "00100\n11110\n10110\n10111\n10101\n01111\n00111\n11100\n10000\n11001\n00010\n01010\n"
test1 = part1 (lines sample)
test2 = part2 (lines sample)

-- Part 1

part1 :: [String] -> Int
part1 input = 
    gamma * epsilon
    where     
        asDigitLists = toDigitLists input
        summedList = sumAllDigitLists asDigitLists
        middlePoint = div (length (input)) 2   
        gamma = binToDec $ map (gammaFilter middlePoint) summedList
        epsilon = binToDec $ map (epsilonFIlter middlePoint) summedList

toDigitLists :: [String] -> [[Int]]
toDigitLists input = map toDigitList input

toDigitList :: String -> [Int]
toDigitList [x] =
    [digitToInt x]
toDigitList (x:xs) = 
    [digitToInt x] ++ toDigitList xs

sumAllDigitLists :: [[Int]] -> [Int]
sumAllDigitLists (x:xs) = foldl sumTwoDigitLists x xs

sumTwoDigitLists :: [Int] -> [Int] -> [Int]
sumTwoDigitLists [x] [y] =
    [x + y]
sumTwoDigitLists (x:xs) (y:ys) =
    [x + y] ++ sumTwoDigitLists xs ys

binToDec :: [Int] -> Int
binToDec list = result
    where (result, _) = foldr binF (0,1) list

binF :: Int -> (Int, Int) -> (Int, Int)
binF x (result, base) = (result + x * base, base * 2)

gammaFilter :: Int -> Int -> Int
gammaFilter middlePoint x =
    if x >= middlePoint
    then 1
    else 0

epsilonFIlter :: Int -> Int -> Int
epsilonFIlter middlePoint x =
    if x < middlePoint
    then 1 
    else 0    

-- Part 2

part2 :: [String] -> [Int]
part2 input = 
    oxyGen
    where     
        asDigitLists = toDigitLists input
        summedList = sumAllDigitLists asDigitLists
        middlePoint = div (length input) 2   
        gamma = map (gammaFilter middlePoint) summedList
        oxyGen = matchByOne asDigitLists

matchByOne :: [[Int]] -> [Int] 
matchByOne [x] = x
matchByOne (x:xs) = 
    matchByOne removedHeads 
    where
        filtered = filter isHeadOne (x:xs)
        removedHeads = map tail filtered

isHeadOne :: [Int] -> Bool
isHeadOne (x:xs) = x == 1
-- Main

day3 = do
    contents <- fmap lines (readFile "../input/3.txt")
    print $ ("Test1: " ++) $ show $ test1
    print $ ("Test2: " ++) $ show $ test2   
    print $ ("Part1: " ++) $ show $ part1 contents
    -- print $ ("Part2: " ++) $ show $ part2 contents 
