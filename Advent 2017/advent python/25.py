tape = [0]
tapePos = 0
state = 'A'
dic = {}

class State:
    def __init__(self, if0f, if0val, if0st, if1f, if1val, if1st):
        self.if0f = if0f
        self.if0val = if0val
        self.if0st = if0st
        self.if1f = if1f
        self.if1val = if1val
        self.if1st = if1st

    def exec(self):
        global tapePos, tape, state, dic
        if tape[tapePos] == 0:
            tape[tapePos] = self.if0val
            self.if0f()
            state = self.if0st
        else:
            tape[tapePos] = self.if1val
            self.if1f()
            state = self.if1st



def moveLeft():
    global tapePos, tape, state, dic
    if tapePos == 0:
        tape.insert(0,0)
    else:
        tapePos -= 1

def moveRight():
    global tapePos, tape, state, dic
    tapePos += 1
    if tapePos >= len(tape)-1:
        tape.append(0)

dic['A'] = State(moveRight,1,'B',moveLeft,0,'F')
dic['B'] = State(moveRight,0,'C',moveRight,0,'D')
dic['C'] = State(moveLeft,1,'D',moveRight,1,'E')
dic['D'] = State(moveLeft,0,'E',moveLeft,0,'D')
dic['E'] = State(moveRight,0,'A',moveRight,1,'C')
dic['F'] = State(moveLeft,1,'A',moveRight,1,'A')

def checkSum():
    global tapePos, tape, state, dic
    cont = 0
    for x in tape:
        if x == 1:
            cont += 1
    print(cont)

def run(iterations):
    for x in range(0,iterations):
        dic[state].exec()
    checkSum()
    return

def test():
    run(12994925)

test()
