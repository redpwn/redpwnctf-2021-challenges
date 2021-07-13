#!/usr/bin/env sage
from Crypto.Util.number import bytes_to_long

a = 2
b = 3
p = 17459102747413984477

E = EllipticCurve(GF(p), [a, b])

d = bytes_to_long(b'm1n1_3cc')

G = E.gens()[0]

Q = d*G

g1,g2,_ = G
q1,q2,_ = Q

#Generate blecc.txt contents
print('p =', p)
print('a =', a)
print('b =', b)
print('G =',(g1,g2))
print('Q =',(q1,q2))
print('d = ???')
print('Can you help me find `d`?')
print('Decode it as a string and wrap in flag format.')

#Solution
assert d == discrete_log(Q,G,operation='+')
