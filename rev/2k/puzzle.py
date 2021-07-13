import z3
from functools import reduce
from random import seed, randint, choice
import json
seed(69420)

f = open("prog.s", "w")

f.write("""; vim: ft=nasm

%include "vmasm.mac"

_start:
\tjump 0x000c
\texit 1
\texit 0
""")



text = "sice deet:\n"

def print_text(text):
    sb = ""
    for i in text:
        if i == "\n":
            sb += f"\tprint 0x000A\n"
        else:
            sb += f"\tprint '{i}'\n"

    f.write(sb)



print_text(text)

with open("settings.json", "r") as jf:
    js = json.load(jf)

printable = "".join(chr(a) for a in range(js["min"], js["max"]))
sz = len(printable)
opchoice = js["opchoice"]
opchoice_not_commute = js["opchoice_nc"]
opchoice_ndiv = js["opchoice_ndiv"]
size_choice = js["size_choice"]


def make_board(size):
    row = []
    for i in range(sz):
        row.append(i+1)
    board = []
    for a in range(sz):
        arow = row[:]
        for k in range(a):
            arow = [arow.pop()] + arow
        board.append(arow)
    for shuf in range(10000):
        r1 = randint(0, sz - 1)
        r2 = r1
        while r2 == r1:
            r2 = randint(0, sz - 1)
        board[r1], board[r2] = board[r2], board[r1]
        b2 = [a[:] for a in board[:]]
        for i in range(sz):
            board[i] = [b2[j][i] for j in range(sz)]
    return board
board = make_board(sz)
for i in range(len(board)):
    for j in range(len(board)):
        board[i][j] = printable[board[i][j]-1]

get_size = lambda : choice(size_choice)

cages = []
for i in range(sz):
    cages.append([])
    for j in range(sz):
        cages[-1].append(-1)

uq = 0
direcs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
from functools import reduce
from random import choice
i, j = 0, 0
boxes = []
while -1 in reduce(lambda a,b: a+b, cages):
    for i in range(sz):
        for j in range(sz):
            if cages[i][j] == -1:
                cages[i][j] = uq
                pos1 = i
                pos2 = j
                adjs = [(a[0]+pos1, a[1]+pos2) for a in direcs if 0 <= a[0]+pos1 <= sz - 1 and 0 <= a[1]+pos2 <= sz - 1]

                vals = []
                for adj in adjs:
                    if cages[adj[0]][adj[1]] == -1:
                        vals.append(adj)
                size = get_size()
                if size == 2:

                    op = choice(opchoice_not_commute)
                    boxes.append([op, uq, [(pos1, pos2)]])
                else:
                    op = choice(opchoice)
                    boxes.append([op, uq, [(pos1, pos2)]])
                index = 1
                while index < size and len(vals) != 0:
                    nbox = choice(vals)
                    pos1 = nbox[0]
                    pos2 = nbox[1]
                    cages[pos1][pos2] = uq

                    adjs = [(a[0]+pos1, a[1]+pos2) for a in direcs if 0 <= a[0]+pos1 <= sz - 1 and 0 <= a[1]+pos2 <= sz - 1]

                    vals = []
                    for adj in adjs:
                        if cages[adj[0]][adj[1]] == -1:
                            vals.append(adj)
                    boxes[-1][2].append((pos1, pos2))
                    index += 1
                uq += 1
                if len(boxes[-1][2]) == 2:
                    poss = boxes[-1][2]
                    largest = printable.index(board[poss[0][0]][poss[0][1]])+1
                    smallest = printable.index(board[poss[1][0]][poss[1][1]])+1
                    if smallest > largest:
                        smallest, largest = largest, smallest
                    if (largest % smallest == 0):
                        boxes[-1][0] = "/"
                    else:
                        boxes[-1][0] = choice(opchoice_ndiv)

with open("sol.txt", "w") as sol:
    for r in board:
        sol.write("".join(r))

exit1 = "\tjump 0x0004\n"
exit0 = "\tjump 0x0008\n"

diff = js["min"] - 1

for i in range(sz):
    for j in range(sz):
        f.write(f"\tload {diff}\n")
        f.write("\tin\n")
        f.write("\tsub\n")
        f.write("\tsto\n")
        f.write("\timp\n")

f.write(f"\tdms {sz**2}\n")

for i in range(sz):
    for j in range(sz):
        for r in range(j):
            f.write(f"\treturn {i*sz + j}\n")
            f.write(f"\treturn {i*sz + r}\n")
            f.write(f"\tsub\n")
            f.write("\tjiz 0x0004\n")
            f.write(f"\treturn {j*sz + i}\n")
            f.write(f"\treturn {r*sz + i}\n")
            f.write(f"\tsub\n")
            f.write("\tjiz 0x0004\n")


val = 0
for i in boxes:
    if len(i[2]) == 1:
        val = printable.index(board[i[2][0][0]][i[2][0][1]]) + 1
        f.write(f"\tload {val}\n")
        f.write(f"\treturn {i[2][0][0]*sz + i[2][0][1]}\n")
        f.write(f"\tsub\n")
        f.write(f"\tjnz 0x0004\n")
    elif i[0] == "+":
        val = sum([printable.index(board[a[0]][a[1]])+1 for a in i[2]])
        f.write(f"\tload {val}\n")
        for coord in i[2]:
            f.write(f"\treturn {coord[0]*sz + coord[1]}\n")
        for c in range(len(i[2])):
            if c != 0:
                f.write(f"\tadd\n")
        f.write(f"\tsub\n")
        f.write(f"\tjnz 0x0004\n")
    elif i[0] == "*":
        val = reduce(lambda a,b:a*b, [printable.index(board[a[0]][a[1]])+1 for a in i[2]])
        f.write(f"\tload {val%32767}\n")
        for coord in i[2]:
            f.write(f"\treturn {coord[0]*sz + coord[1]}\n")
        for c in range(len(i[2])):
            if c != 0:
                f.write(f"\tmmod 32767\n")
        f.write(f"\tsub\n")
        f.write(f"\tjnz 0x0004\n")

    elif i[0] == "-" and len(i[2]) == 2:
        val = abs(printable.index(board[i[2][0][0]][i[2][0][1]]) - printable.index(board[i[2][1][0]][i[2][1][1]]))
        f.write(f"\tload {val}\n")
        for coord in i[2]:
            f.write(f"\treturn {coord[0]*sz + coord[1]}\n")
        for c in range(len(i[2])):
            if c != 0:
                f.write(f"\tsub\n")
        f.write(f"\tdup\n")
        f.write(f"\tsig\n")
        f.write(f"\tmul\n")
        f.write(f"\tsub\n")
        f.write(f"\tjnz 0x0004\n")
    elif i[0] == "/" and len(i[2]) == 2:
        a = printable.index(board[i[2][0][0]][i[2][0][1]])+1
        b = printable.index(board[i[2][1][0]][i[2][1][1]])+1
        if a % b == 0:
            val = a // b
        else:
            val = b // a
        f.write(f"\tload {val}\n")
        for coord in i[2]:
            f.write(f"\treturn {coord[0]*sz + coord[1]}\n")
        f.write(f"\tmod\n")
        for coord in i[2][::-1]:
            f.write(f"\treturn {coord[0]*sz + coord[1]}\n")
        f.write(f"\tmod\n")
        f.write(f"\tmul\n")
        f.write(f"\tjnz 0x0004\n")
        for coord in i[2]:
            f.write(f"\treturn {coord[0]*sz + coord[1]}\n")
        f.write(f"\tneq\n")
        f.write(f"\tload 1\n")
        f.write(f"\tadd\n")
        for coord in i[2]:
            f.write(f"\treturn {coord[0]*sz + coord[1]}\n")
        f.write(f"\tdiv\n")
        for coord in i[2][::-1]:
            f.write(f"\treturn {coord[0]*sz + coord[1]}\n")
        f.write(f"\tdiv\n")
        f.write(f"\tadd\n")
        f.write(f"\tdiv\n")
        f.write(f"\tsub\n")
        f.write(f"\tjnz 0x0004\n")


f.write(f"\tjump 0x0008\n")

f.close()



