#!/usr/bin/env python3

import z3
import random

CONSTRAINTS = 250

flag = open('flag.txt', 'rb').read().strip()

def gen():
  idx = list(range(len(flag)))
  while True:
    random.shuffle(idx)
    for i in idx:
      yield i

def pair(g):
  a = next(g)
  while (b := next(g)) == a: pass
  return a, b

chars = [z3.BitVec(f'c{i}', 8) for i in range(len(flag))]
s = z3.Solver()
for i, v in enumerate(flag):
  if i < len('flag'):
    s.add(chars[i] == v)
  s.add(chars[i] > 0x20)
  s.add(chars[i] < 0x7f)

def ge_le(a, b):
  if flag[a] <= flag[b]:
    return (chars[a] <= chars[b], (a, b, 'le'))
  return (chars[a] >= chars[b], (a, b, 'ge'))

def eq_ne(a, b):
  if flag[a] == flag[b]:
    return (chars[a] == chars[b], (a, b, 'eq'))
  return (chars[a] != chars[b], (a, b, 'ne'))

def add(a, b):
  return (chars[a] + chars[b] == flag[a] + flag[b], (a, b, 'add'))

def sub(a, b):
  if flag[a] < flag[b]:
    a, b = b, a
  return (chars[a] - chars[b] == flag[a] - flag[b], (a, b, 'sub'))

def xor(a, b):
  return (chars[a] ^ chars[b] == flag[a] ^ flag[b], (a, b, 'xor'))

funcs = [ge_le, eq_ne, add, sub, xor]

g = gen()
z3cons, sercons = list(zip(*(random.choice(funcs)(*pair(g)) for _ in range(CONSTRAINTS))))

for c in z3cons:
  s.add(c)

# this should always be sat
assert s.check() == z3.sat, 'gen not sat'

# this should be unsat so there are no other solutions
s.add(z3.Or(*(chars[i] != v for i, v in enumerate(flag) if i >= len('flag'))))
assert s.check() == z3.unsat, 'gen not fully constrained'

# test solve
test_s = z3.Solver()
for i, v in enumerate(flag):
  if i < len('flag'):
    test_s.add(chars[i] == v)
  test_s.add(chars[i] > 0x20)
  test_s.add(chars[i] < 0x7f)

for c in z3cons:
  test_s.add(c)

assert test_s.check() == z3.sat, 'test not sat'

# flag should be same
m = test_s.model()
test_flag = bytes(m[c].as_long() for c in chars)

assert test_flag == flag, 'test flag wrong'

import json
with open('constraints.json', 'w') as f:
  json.dump(sercons, f)
