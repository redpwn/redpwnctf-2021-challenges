#!/usr/bin/env python3

from pwn import remote, args

host = args.HOST or 'localhost'
port = args.PORT or 31845

def receiver(*args, **kwargs):
  r = remote(*args, **kwargs)
  last = True
  count = 0
  while True:
    try:
      c = r.recv(1)
    except EOFError:
      return
    on = (c[0] == 7)
    if on == last:
      count += 1
    else:
      yield last, count
      last = on
      count = 1

msg = ''
def p(s):
  global msg
  msg += s
  print(s, end='', flush=True)

l2s = {
  (False, 1): '',
  (False, 3): ' ',
  (False, 7): ' / ',
  (True, 1): '.',
  (True, 3): '-',
}
for t in receiver(host, port):
  p(l2s[t])
print()

morse = {
  '.-': 'a', '-...': 'b', '-.-.': 'c', '-..': 'd', '.': 'e', '..-.': 'f',
  '--.': 'g', '....': 'h', '..': 'i', '.---': 'j', '-.-': 'k', '.-..': 'l',
  '--': 'm', '-.': 'n', '---': 'o', '.--.': 'p', '--.-': 'q', '.-.': 'r',
  '...': 's', '-': 't', '..-': 'u', '...-': 'v', '.--': 'w', '-..-': 'x',
  '-.--': 'y', '--..': 'z', '.----': '1', '..---': '2', '...--': '3',
  '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8',
  '----.': '9', '-----': '0', '.-...': '&', '.----.': "'", '.--.-.': '@',
  '-.--.-': '}', '-.--.': '{', '---...': ':', '--..--': ',', '-...-': '=',
  '-.-.--': '!', '.-.-.-': '.', '-....-': '-', '.-.-.': '+', '.-..-.': '"',
  '..--..': '?', '-..-.': '/',
}

print(' '.join(''.join(morse.get(c, '') for c in word.split()) for word in msg.split(' / ')))
