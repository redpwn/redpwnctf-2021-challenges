from pwn import *


crc_table = list()

def make_crc_table():
    c = ''
    for n in range(0,256):
        c = n
        for k in range(0,8):
            if (c & 1) == 1:
                c = 0xedb88320 ^ (c >> 1)
            else:
                c = c >> 1
        crc_table.append(c)


def update_crc(byte, bufLen):
    c = 0xffffffff;
    for n in range(0,bufLen):
        c = crc_table[(c ^ byte[n]) & 0xff] ^ (c >> 8);
    return c ^ 0xffffffff;
#extracted bytes from gdb
f = open('newbytes')
x = f.readlines()
y = bytearray()
for i in x:
        for thing in i.strip().replace(" ","").split("0x"):
                if len(thing)>1:
                        y.append(int(thing,16))

#write IDAT chunk 
binary = open('newpng','r+b')
print(len(y))
for i in range(0,256):
        for j in range(0,256):
                y[500] = i
                y[501] = j
                if (update_crc(y,971) & 0xffff) == 0x1814:
                        print('WINNER')
                        print(i)
                        print(j)
                        print(len(y))
                        break

#values found (must reinvert then write to file)
y[500] = 147
y[501] = 144
for i in range(4,len(y)):
        y[i] = ~y[i]&0xff
print(y)
binary.seek(0)
binary.write(y)


#i just copy pasted a valid header at the top of the file and got rid of the stuff after the IEND chunk manually here


with open('payload.png', 'r+b') as f:
    f = f.read()

    p = process('./chal')
    p.recvuntil('your file?')
    p.sendline(str(len(f)))
    p.recvuntil('send your image here:')
    p.send(f)
    p.send('y')
    p.interactive()

