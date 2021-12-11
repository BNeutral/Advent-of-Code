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
        middlePoint = div (length input) 2
        gamma = binToDec $ map (gammaFilter middlePoint) summedList
        epsilon = binToDec $ map (epsilonFIlter middlePoint) summedList

toDigitLists :: [String] -> [[Int]]
toDigitLists = map toDigitList

toDigitList :: String -> [Int]
toDigitList [x] =
    [digitToInt x]
toDigitList (x:xs) =
    digitToInt x : toDigitList xs

sumAllDigitLists :: [[Int]] -> [Int]
sumAllDigitLists (x:xs) = foldl (zipWith (+)) x xs

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

part2 :: [String] -> (Int,[Int])
part2 input =
    (middlePoint, summedList)
    -- asDigitListsEnumerated !! oxyId
    where
        asDigitLists = toDigitLists input
        asDigitListsEnumerated = zip [0..] asDigitLists
        summedList = sumAllDigitLists asDigitLists
        middlePoint = div (length input) 2
        gamma = map (gammaFilter middlePoint) summedList
        epsilon = map (epsilonFIlter middlePoint) summedList
        oxyId = matchByList asDigitListsEnumerated gamma
        co2Id = matchByList asDigitListsEnumerated epsilon

matchByList :: [(Int, [Int])] -> [Int] -> Int
matchByList [(id, x)] (o:os) = id
matchByList [(id, x)] [] = id
matchByList ((id,x:xs):next) (o:os) =
    matchByList (removeHeads $ filterByNum ((id,x:xs):next) o) os

removeHeads :: [(Int, [Int])] -> [(Int, [Int])]
removeHeads [(id,x:xs)] = [(id,xs)]
removeHeads ((id,x:xs):next) =
    (id,xs) : removeHeads next

filterByNum :: [(Int, [Int])] -> Int -> [(Int, [Int])]
filterByNum [(id,x:xs)] filterVal =
    [(id,x:xs) | x == filterVal]
filterByNum ((id,x:xs):next) filterVal =
    if x == filterVal
    then (id,x:xs) : filterByNum next filterVal
    else filterByNum next filterVal

filterParse :: [(Int, [Int])] -> [(Int, [Int])]
filterParse [(id,x:xs)] = [(id,x:xs)]
filterParse input =
    (1,summedList)
    where
        summed = map ((+) . head . snd) input
        middlePoint = div (length input) 2
        oxy = gammaFilter middlePoint summed
        co2 = epsilonFIlter middlePoint summed
        oxyId = matchByList asDigitListsEnumerated gamma
        co2Id = matchByList asDigitListsEnumerated epsilon

-- Main

day3 = do
    contents <- fmap lines (readFile "../input/3.txt")
    print $ ("Test1: " ++) $ show test1
    print $ ("Test2: " ++) $ show test2
    print $ ("Part1: " ++) $ show $ part1 contents
    --print $ ("Part2: " ++) $ show $ part2 contents
