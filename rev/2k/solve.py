import z3
from functools import reduce
from itertools import product
import json

with open('prog.s', 'r') as f:
    disasm = f.read()

disasm = disasm.split("\tjnz 0x0004")
disasm[0] = disasm[0].split("\tjiz 0x0004")[-1]
del disasm[-1]


nd = []
for i in range(len(disasm)):
    if "neq" in disasm[i]:
        nd.append(disasm[i-1] + disasm[i])
    elif "mmod" in disasm[i]:
        nd.append(disasm[i])
    elif "mod" in disasm[i]:
        pass
    else:
        nd.append(disasm[i])

with open("settings.json", "r") as f:
    js = json.load(f)
printable = "".join(chr(a) for a in range(js["min"], js["max"]))
size = len(printable)
disasm = nd[:]
board = [[z3.Int(f'r{r}c{c}') for c in range(size)] for r in range(size)]
brd = [[-1 for c in range(size)] for r in range(size)]

s = z3.Solver()

for r, c in product(range(size), range(size)):
    s.add(board[r][c] >= 1)
    s.add(board[r][c] <= size)

for i in range(size):
    s.add(z3.Distinct(*board[i]))
    s.add(z3.Distinct(*(board[r][i] for r in range(size))))


def z3abs(x):
    return z3.If(x >= 0, x, -x)

def kendiv(a, b, y):
    return z3.Or(a*y == b, b*y == a)

counter = 0
boxes = []
i = 0
for i in disasm:
    print(i)
    if "neq" in i:
        pos = []
        val = int(i.strip().split("\n")[0].replace("load", ""))
        for j in i.split("\n"):
            if "return" in j: 
                ordin = int(j.replace("return", ""))
                y = ordin // size
                x = ordin % size
                if len(pos) < 2:
                    pos.append((y, x))
        boxes.append((pos, "div", val, counter, "/"))
        counter += 1
        print("/", pos, val)
        s.add(kendiv(board[pos[0][0]][pos[0][1]], board[pos[1][0]][pos[1][1]], val))
        for q in pos:
            brd[q[0]][q[1]] = counter
    elif "sig" in i: 
        pos = []
        val = int(i.strip().split("\n")[0].replace("load", ""))
        for j in i.split("\n"):
            if "return" in j: 
                ordin = int(j.replace("return", ""))
                y = ordin // size
                x = ordin % size
                if len(pos) < 2:
                    pos.append((y, x))
        boxes.append((pos, "sub", val, counter, "-"))
        counter += 1
        print("-", pos, val)
        s.add(z3abs(board[pos[0][0]][pos[0][1]] - board[pos[1][0]][pos[1][1]]) == val)
        for q in pos:
            brd[q[0]][q[1]] = counter
    elif "mmod" in i: 
        pos = []
        val = int(i.strip().split("\n")[0].replace("load", ""))
        for j in i.split("\n"):
            if "return" in j: 
                ordin = int(j.replace("return", ""))
                y = ordin // size
                x = ordin % size
                #
                pos.append((y, x))
        boxes.append((pos, "mul", val, counter, "*"))
        counter += 1
        print("*", pos, val)
        s.add(reduce(lambda x,y:x*y, [board[r[0]][r[1]] for r in pos]) % 32767 == val)
        for q in pos:
            brd[q[0]][q[1]] = counter
    elif "add" in i:
        pos = []
        val = int(i.strip().split("\n")[0].replace("load", ""))
        for j in i.split("\n"):
            if "return" in j: 
                ordin = int(j.replace("return", ""))
                y = ordin // size
                x = ordin % size
                #
                pos.append((y, x))
        boxes.append((pos, "add", val, counter, "+"))
        print("+", pos, val)
        s.add(sum([board[r[0]][r[1]] for r in pos]) == val)
        for q in pos:
            brd[q[0]][q[1]] = counter
    else: 
        pos = (0, 0)
        val = int(i.strip().split("\n")[0].replace("load", ""))
        for j in i.split("\n"):
            if "return" in j:
                ordin = int(j.replace("return", ""))
                y = ordin // size
                x = ordin % size
                # 
                pos = (y, x)
        print("=", [pos], val)
        boxes.append(([pos], "add", val, counter, "#"))
        s.add(board[pos[0]][pos[1]] == val)
        #
        brd[pos[0]][pos[1]] = counter
    counter += 1

assert s.check() == z3.sat


m = s.model()
for r in range(size):
    for c in range(size):
        print(chr(m[board[r][c]].as_long() - 1 + js["min"]), end="")
