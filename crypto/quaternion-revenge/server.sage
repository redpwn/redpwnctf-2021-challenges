#!/usr/bin/env sage
from Crypto.Util.number import getPrime, bytes_to_long
import secrets
import asyncio

with open('flag.txt','r') as flagfile:
    flag = flagfile.read().strip()

with open('secret.txt','rb') as secret:
    M = secret.read().strip()
glob_m = bytes_to_long(M)

async def handle_conn(reader, writer):

    async def print(ptext):
        writer.write((ptext+'\n').encode())

    async def prompt(ptext):
        writer.write(ptext.encode())
        await writer.drain()
        return (await reader.readline()).decode().strip()

    p = getPrime(512)
    q = getPrime(512)
    n = p * q
    e = 65537
    Q.<i,j,k> = QuaternionAlgebra(-p,-q)

    #randomize M per-instance
    m = glob_m ^^ secrets.randbelow(n)

    #prepare leaks
    n  = n
    l  = m.bit_length()
    c1 = pow(m,e,p)
    c2 = pow(m,e,q)

    #reveal leaks
    await print(f'n: {n}')
    await print(f'l: {l}')
    await print(f'c1: {c1}')
    await print(f'c2: {c2}')

    #Present challenge
    try:
        await print("Calculate the left quaternion isomorphism of m:")
        inp = await prompt('>>> ')
        assert all([x in '1234567890 ijk*+' for x in inp])
        user_quat = eval(inp)
        if user_quat==m:
            await print(flag)
        else:
            await print('Wrong!')
    except Exception:
        await print("Error or timed out.")
    finally:
        await writer.drain()
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_conn, '0.0.0.0', 9999)
    addr = server.sockets[0].getsockname()
    print(f'Listening on {addr}')
    async with server:
        await server.serve_forever()

asyncio.run(main())
