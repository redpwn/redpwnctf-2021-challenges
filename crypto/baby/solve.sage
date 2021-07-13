from Crypto.Util.number import long_to_bytes

with open('output.txt') as f:
  nums = f.read().splitlines()

n, e, c = (Integer(line.split()[1]) for line in nums)
(p, _), (q, _) = factor(n)
d = inverse_mod(e, (p-1)*(q-1))
m = power_mod(c, d, n)

print(long_to_bytes(m).decode())
