#!/usr/bin/env sage
from Crypto.Util.number import long_to_bytes
import json

#Definition
n = 25_000
Sn = SymmetricGroup(n)

#Interaction
with open('output.json','r') as f:
    givens = json.load(f)
g = Sn(givens['g'])
h = Sn(givens['h'])
t1 = Sn(givens['t1'])
t2 = Sn(givens['t2'])

#Solution
pi = g.cycle_tuples(singletons=True)
sigma = h.cycle_tuples(singletons=True)
G = [(j:=[x for x in pi if i in x][0], j.index(i)) for i in range(1,n+1)]
H = [(k:=[x for x in sigma if i in x][0], k.index(i)) for i in range(1,n+1)]
First = [sigma[j][0]for j in range(len(sigma))]
Second = [sigma[j][1%len(sigma[j])]for j in range(len(sigma))]
D = []
L = []
for j in range(len(sigma)):
    pi_j = [x for x in pi if First[j] in x][0]
    D.append(pi_j.index(Second[j])-pi_j.index(First[j]))
    L.append(len(pi_j))
a = CRT(D,L)
m = t2 * (t1^-a)
M = 'flag{' + long_to_bytes(Permutation(m).rank()).split(b'flag{')[-1].decode()

#Display
print(M)
