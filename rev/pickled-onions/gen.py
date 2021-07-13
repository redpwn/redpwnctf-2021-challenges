#!/usr/bin/env python3

import json
with open('constraints.json') as f:
  constraints = json.load(f)
flag = open('flag.txt', 'rb').read().strip()

from pickle import *
import random

DEBUG = False
SYMBOLS = {}
veggies = open('veggies.txt').read().splitlines()
random.seed(20201125)
random.shuffle(veggies)
def sym(s):
  if DEBUG: return s
  if s not in SYMBOLS:
    SYMBOLS[s] = 'pickled' + veggies.pop()
  return SYMBOLS[s]

p32 = lambda x: x.to_bytes(4, 'little')           # converts int32 to bytes
p8 = lambda x: x.to_bytes(1, 'little')            # converts int8 to bytes
nl = lambda s: s.encode() + b'\n'                 # converts str to NL-terminated bytes
uni = lambda s: SHORT_BINUNICODE + p8(len(s)) + s.encode() if len(s) < 256 else \
  BINUNICODE + p32(len(s)) + s.encode()           # converts str to pickle BINUNICODE or SHORT_BINUNICODE
bnb = lambda b: SHORT_BINBYTES + p8(len(b)) + b if len(b) < 256 else \
  BINBYTES + p32(len(b)) + b                      # converts bytes to pickle BINBYTES or SHORT_BINBYTES
it = lambda i: INT + nl(str(i))                   # converts int to pickle INT
get = lambda i: GET + nl(str(i))                  # GETs index i from memo
put = lambda i: PUT + nl(str(i))                  # PUTs at index i in memo
get_global = lambda x, y: GLOBAL + nl(x) + nl(y)  # pickle GLOBAL

# pickle module is used to store variables
# actually it's not the pickle module anymore but I don't want to change variable names
pickle_module = get_global('pickle', 'io')

# setattr on whatever is on top of the stack
# typically use pickle_module + set_var()
set_var = lambda *args: \
  MARK + \
    b''.join(args) + \
    DICT + \
  BUILD

# getattr on pickle module
# can also be used for pickle.loads
get_var = lambda x: get_global('io', x)

# only need two registers lmao
regs = [sym(f'reg{i}') for i in range(2)]

# used for branching
branch = sym('branch')

# checker funcs
checker_proto = PROTO + b'\x04' + \
  pickle_module + \
  get_var(regs[0] + '.__OPERATION__') + \
    get_var(regs[1]) + TUPLE1 + \
  REDUCE + STOP

add = checker_proto.replace(b'OPERATION', b'add')
sub = checker_proto.replace(b'OPERATION', b'sub')
xor = checker_proto.replace(b'OPERATION', b'xor')
arith = {
  'add': lambda a, b: flag[a] + flag[b],
  'sub': lambda a, b: flag[a] - flag[b],
  'xor': lambda a, b: flag[a] ^ flag[b],
}

eq = checker_proto.replace(b'OPERATION', b'eq')
ne = checker_proto.replace(b'OPERATION', b'ne')
le = checker_proto.replace(b'OPERATION', b'le')
ge = checker_proto.replace(b'OPERATION', b'ge')

# pops correct number of chars, then puts in memo
def pop_args(*args):
  argpos = {v: i for i, v in enumerate(args)}
  ret = b''
  pos = len(flag) # 1 greater than current
  while pos:
    if pos-1 in argpos:
      ret += put(argpos[pos-1])
    ret += POP
    pos -= 1
  return ret

def gen_checker(a, b, op, falsebranch, truebranch):
  checker = pop_args(a, b) + \
    pickle_module + \
    set_var(
      uni(regs[0]), get(0),
      uni(regs[1]), get(1),
      uni(branch), falsebranch + truebranch + TUPLE2,
    ) + \
    get_global('pickle', 'loads') + \
      uni('io') + \
      get_var(branch + '.__getitem__')
  if op in arith:
    checker += pickle_module + set_var(
      uni(regs[0]),
        get_global('pickle', 'loads') + \
          get_var(sym(f'{op}_eval')) + \
        TUPLE1 + REDUCE,
      uni(regs[1]),
        it(arith[op](a, b)),
    ) + POP
    comp = 'eq'
  else:
    comp = op
  checker += get_global('pickle', 'loads') + \
    get_var(sym(f'{comp}_eval')) + \
  TUPLE1 + REDUCE + TUPLE1 + REDUCE + STACK_GLOBAL + TUPLE1 + REDUCE + STOP
  return checker

success = it(1) + STOP
fail = it(0) + STOP

run_checks = PROTO + b'\x04' + \
  pickle_module + \
  set_var(
    uni(sym('input')),
      get_var(sym('delim') + '.join') + \
        get_global('builtins', 'map') + \
          get_global('builtins', 'str') + \
          get_var(sym('input')) + \
        TUPLE2 + REDUCE + \
      TUPLE1 + REDUCE
  ) + \
  set_var(
    uni(sym('input')),
      get_var(sym('input') + '.encode') + \
      EMPTY_TUPLE + REDUCE
  ) + \
  set_var(
    uni(sym('base')),
      get_var(sym('base') + '.__add__') + \
        get_var(sym('input')) + \
      TUPLE1 + REDUCE
  ) + \
  set_var(
    uni(sym('base')),
      get_var(sym('base') + '.__add__') + \
        bnb(b'\n') + \
      TUPLE1 + REDUCE
  )

run_checks += set_var(
  uni(sym('printable_check')), get_var(sym('base')),
  uni(sym('printable')), it(1),
)

for _ in range(len(flag)):
  run_checks += set_var(
    uni(sym('printable_check')), get_var(sym('printable_check')+'.__add__') + \
      bnb(
        put(0) + POP +
        pickle_module + \
        set_var(uni(regs[0]), get(0)) + \
        set_var(
          uni(sym('printable')), get_var(sym('printable')+'.__and__') + \
            get_var(regs[0]+'.__gt__') + it(0x20) + TUPLE1 + REDUCE + TUPLE1 + REDUCE
        ) + \
        set_var(
          uni(sym('printable')), get_var(sym('printable')+'.__and__') + \
            get_var(regs[0]+'.__lt__') + it(0x7f) + TUPLE1 + REDUCE + TUPLE1 + REDUCE
        ) + POP
      ) + TUPLE1 + REDUCE
  )

run_checks += set_var(
  uni(sym('printable_check')), get_var(sym('printable_check')+'.__add__') + \
    bnb(get_var(sym('printable')) + STOP) + TUPLE1 + REDUCE
)

sanity = [
  uni(sym('sanity_printable')),
  bnb(
    PROTO + b'\x04' + pickle_module + \
    set_var(
      uni(branch), uni(sym('fail')) + uni(sym('sanity0')) + TUPLE2,
    ) + \
    get_global('pickle', 'loads') + \
      uni('io') + \
      get_var(branch + '.__getitem__') + \
        get_global('pickle', 'loads') + get_var(sym('printable_check')) + TUPLE1 + REDUCE + \
      TUPLE1 + REDUCE + \
      STACK_GLOBAL +
    TUPLE1 + REDUCE + STOP
  ),
]

for i, v in enumerate(flag[:len('flag')]):
  sanity.append(uni(sym(f'sanity{i}')))
  falsebr = uni(sym('fail'))
  if i == len('flag') - 1:
    truebr = uni(sym('check0'))
  else:
    truebr = uni(sym(f'sanity{i+1}'))
  sanity.append(
    get_var(sym('base')+'.__add__') + \
      bnb(
        pop_args(i) + \
        pickle_module + \
        set_var(
          uni(regs[0]), get(0),
          uni(regs[1]), it(v),
          uni(branch), falsebr + truebr + TUPLE2,
        ) +
        get_global('pickle', 'loads') + \
          uni('io') + \
          get_var(branch + '.__getitem__') + \
            get_global('pickle', 'loads') + get_var(sym('eq_eval')) + TUPLE1 + REDUCE + \
          TUPLE1 + REDUCE + \
          STACK_GLOBAL + \
        TUPLE1 + REDUCE + STOP
      ) + \
    TUPLE1 + REDUCE
  )
run_checks += set_var(*sanity)

checks = []
for i, (a, b, op) in enumerate(constraints):
  checks.append(uni(sym(f'check{i}')))
  falsebr = uni(sym('fail'))
  if i == len(constraints) - 1:
    truebr = uni(sym('success'))
  else:
    truebr = uni(sym(f'check{i+1}'))
  checks.append(
    get_var(sym('base')+'.__add__') + bnb(
      gen_checker(a, b, op, falsebr, truebr)
    ) + TUPLE1 + REDUCE
  )
run_checks += set_var(*checks)

run_checks += get_global('pickle', 'loads') + get_var(sym('sanity_printable')) + TUPLE1 + REDUCE + STOP

prog = PROTO + b'\x04' + \
  pickle_module + \
  set_var(
    uni(sym('add_eval')), bnb(add),
    uni(sym('sub_eval')), bnb(sub),
    uni(sym('xor_eval')), bnb(xor),
    uni(sym('eq_eval')), bnb(eq),
    uni(sym('ne_eval')), bnb(ne),
    uni(sym('le_eval')), bnb(le),
    uni(sym('ge_eval')), bnb(ge),
    uni(sym('success')), bnb(success),
    uni(sym('fail')), bnb(fail),
    uni(sym('base')), bnb(b'\x80\x04I'),
    uni(sym('run_checks')), bnb(run_checks),
    uni(sym('delim')), SHORT_BINUNICODE + b'\x02' + b'\nI',
    uni(sym('msg')), uni('Nope!') + uni('Correct!') + TUPLE2,
    uni(sym('input')),
      get_global('builtins', 'input') + \
        uni('What is the flag? ') + \
      TUPLE1 + REDUCE,
    uni(branch), uni(sym('fail')) + uni(sym('run_checks')) + TUPLE2,
  ) + \
  set_var(
    uni(sym('input_len')),
      get_var(sym('input')+'.__len__') + \
      EMPTY_TUPLE + REDUCE,
    uni(sym('input')),
      get_var(sym('input')+'.encode') + \
      EMPTY_TUPLE + REDUCE
  ) + \
  get_global('builtins', 'print') + \
    get_var(sym('msg')+'.__getitem__') + \
      get_global('pickle', 'loads') + \
        uni('io') + \
        get_var(branch + '.__getitem__') + \
          get_var(sym('input_len')+'.__eq__') + \
            it(len(flag)) + \
          TUPLE1 + REDUCE + \
        TUPLE1 + REDUCE + \
        STACK_GLOBAL + \
      TUPLE1 + REDUCE + \
    TUPLE1 + REDUCE + \
  TUPLE1 + REDUCE + \
  STOP

if b'leeks' not in prog:
  raise ValueError('wtmoo')

wrapped = \
  MARK + \
    b'I' + '\nI'.join(map(str, prog)).encode() + b'\n' + \
    TUPLE + \
  PUT + b'69420\n' + \
  get_global('pickle', 'loads') + \
    get_global('builtins', 'bytes') + \
      GET + b'69420\n' + \
    TUPLE1 + REDUCE + \
  TUPLE1 + REDUCE + STOP

with open('chall.py', 'w') as f:
  f.write(f'__import__(\'pickle\').loads({wrapped})')
