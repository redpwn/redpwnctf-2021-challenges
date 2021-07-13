from pwn import *
import sys
from pathlib import Path

filename, host, port = sys.argv[1:]

contents = Path(filename).read_bytes()

p = remote(host, port)
p.send(p16(len(contents)) + contents)
p.interactive()
