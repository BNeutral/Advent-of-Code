module Day1 where

-- Tests

sample = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
test1 = part1 sample
test2 = part2 sample

-- Part 1

part1 :: [Int] -> Int
part1 list = subPart1 list 0 0

subPart1 :: [Int] -> Int -> Int -> Int
subPart1 [] previousNumber totalIncreasing = totalIncreasing - 1 -- We are counting the first one that isn't an increase as if it was
subPart1 (x:rest) previousNumber totalIncreasing =
    if x > previousNumber 
    then subPart1 rest x (totalIncreasing + 1)
    else subPart1 rest x totalIncreasing

-- Part 2

part2 :: [Int] -> Int
part2 list = subPart2 list 0 0

subPart2 :: [Int] -> Int -> Int -> Int
subPart2 (x:y:[]) previousSum totalIncreasing = totalIncreasing - 1 -- We are counting the first one that isn't an increase as if it was
subPart2 (x:y:z:rest) previousSum totalIncreasing =
    if currentSum > previousSum
    then subPart2 (y:z:rest) currentSum (totalIncreasing + 1)
    else subPart2 (y:z:rest) currentSum totalIncreasing
    where currentSum = x + y + z

-- Main

day1 = do
    contents <- fmap lines (readFile "input/1.txt")
    print $ ("Test1: " ++) $ show $ test1    
    print $ ("Part1: " ++) $ show $ part1 $ fmap read contents
    print $ ("Test2: " ++) $ show $ test2   
    print $ ("Part2: " ++) $ show $ part2 $ fmap read contents 
