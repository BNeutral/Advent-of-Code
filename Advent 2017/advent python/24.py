class Piece:
    def __init__(self,x,y): 
            self.x = x
            self.y = y

def getData():
    f = open("./input/input24","r")
    v = []
    for line in f:
        line=line.strip()
        v.append(line)
    f.close()
    return strArrayToPieces(v)

def toPiece(s):
        r = s.split("/")
        return Piece(int(r[0]),int(r[1]))

def strArrayToPieces(lines):
    r = []
    c = 0
    for x in lines:
        r.append(toPiece(x))  
        c += 1
    return r

def solve(available, path, resultArray):
    ended = True
    for piece in available:
        if piece.x == path[-1]:
            a = set(available)
            a.remove(piece)
            p = list(path)
            p.append(piece.x)
            p.append(piece.y)
            ended = False
            solve(a, p, resultArray)
        if piece.y == path[-1]:
            a = set(available)
            a.remove(piece)
            p = list(path)
            p.append(piece.y)
            p.append(piece.x)
            ended = False
            solve(a, p, resultArray)
    if ended:
            resultArray.append(path)

def main():
    data = getData()
    solveForData(data)

def test():
    lines=["0/2","2/2","2/3","3/4","3/5","0/1","10/1","9/10"]
    data = strArrayToPieces(lines)
    solveForData(data)

def solveForData(data):
    available = set(data)
    path = [0]
    res = []
    solve(available, path, res)
    maxx = 0
    lenn = 0
    for x in res:
        if len(x) > lenn:
                lenn = len(x)
    for x in res:
        if len(x) >= lenn:    
            suma = sum(x)
            if (suma > maxx):
                maxx = suma
    print(maxx)

main()
