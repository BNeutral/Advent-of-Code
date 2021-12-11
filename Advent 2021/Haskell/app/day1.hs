module Day1 where

-- Tests

sample = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
test1 = part1_v2 sample
test2 = part2_v2 sample

-- Part 1

part1 :: [Integer] -> Integer
part1 list = subPart1 list 0 0

subPart1 :: [Integer] -> Integer -> Integer -> Integer
subPart1 [] previousNumber totalIncreasing = totalIncreasing - 1 -- We are counting the first one that isn't an increase as if it was
subPart1 (x:rest) previousNumber totalIncreasing =
    if x > previousNumber
    then subPart1 rest x (totalIncreasing + 1)
    else subPart1 rest x totalIncreasing

-- Part 2

part2 :: [Integer] -> Integer
part2 list = subPart2 list 0 0

subPart2 :: [Integer] -> Integer -> Integer -> Integer
subPart2 [x, y] previousSum totalIncreasing = totalIncreasing - 1 -- We are counting the first one that isn't an increase as if it was
subPart2 (x:y:z:rest) previousSum totalIncreasing =
    if currentSum > previousSum
    then subPart2 (y:z:rest) currentSum (totalIncreasing + 1)
    else subPart2 (y:z:rest) currentSum totalIncreasing
    where currentSum = x + y + z

-- Both parts, just to have the window less hardcoded at the cost of efficiency

part1_v2 :: [Integer] -> Integer
part1_v2 list = subPart list 0 0 1
part2_v2 :: [Integer] -> Integer
part2_v2 list = subPart list 0 0 3

subPart :: [Integer] -> Integer -> Integer -> Int -> Integer
subPart list previousSum totalIncreasing windowSize
  | length window < windowSize = totalIncreasing - 1
  | currentSum > previousSum = subPart xs currentSum (totalIncreasing + 1) windowSize
  | otherwise = subPart xs currentSum totalIncreasing windowSize
  where
      x = head list
      xs = tail list
      window = take windowSize list
      currentSum = sum window

-- Another version for part 1

part1_v3 :: [Integer] -> Integer
part1_v3 list =
    acum - 1
    where (_,acum) = foldl foldCmp (0,0) list

foldCmp :: (Integer,Integer) -> Integer -> (Integer,Integer)
foldCmp (previousNumber, acum) newNumber =
    if newNumber > previousNumber
        then (newNumber, acum+1)
        else (newNumber, acum)

-- Main

day1 = do
    contents <- fmap lines (readFile "../input/1.txt")
    print $ ("Test1: " ++) $ show test1
    print $ ("Test2: " ++) $ show test2
    -- print $ ("Part1: " ++) $ show $ part1 $ fmap read contents
    -- print $ ("Part2: " ++) $ show $ part2 $ fmap read contents 
    print $ ("Part1: " ++) $ show $ part1_v2 $ fmap read contents
    print $ ("Part2: " ++) $ show $ part2_v2 $ fmap read contents
    -- rint $ ("Part1: " ++) $ show $ part1_v3 $ fmap read contents
