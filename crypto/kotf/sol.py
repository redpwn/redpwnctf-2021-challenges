from pwn import *
from subprocess import check_output
import sympy
from math import gcd

host = args.HOST or 'localhost'
port = args.PORT or 31538

if args.LOCAL:
  r = process('python3 ./kotf.py', shell=True)
else:
  r = remote(host, port)
  r.recvuntil('proof of work: ')
  r.sendafter('solution: ', check_output(r.recvline(), shell=True))
  log.info('pow done')

A = open('mA', 'rb')
B = open('mB', 'rb')
a = A.read()
b = B.read()

p = int(r.recvline())
q = int(r.recvline())
g = int(r.recvline())

y = int(r.recvline())

r.recvline()

r.sendline(a.hex())


h1 = int(r.recvline())
r1 = int(r.recvline())
s1 = int(r.recvline())

r.recvline()

r.sendline(b.hex())
h2 = int(r.recvline())
r2 = int(r.recvline())
s2 = int(r.recvline())

r.recvline()
r.recvline()
r.recvline()

mhash =  r.recvline()[12:]


ma = sympy.Matrix([[s1, q-r1], [s2, q-r2]])
mb = sympy.Matrix([h1, h2-s2])

det = int(ma.det())
ans = pow(det, q-2, q) * ma.adjugate() @ mb % q

x = ans[1]

k = 5
R = pow(g, k, p) % q
S = (pow(k, q - 2, q) * (int(mhash) + x * R)) % q

r.sendline(str(R))
r.sendline(str(S))

r.interactive()
