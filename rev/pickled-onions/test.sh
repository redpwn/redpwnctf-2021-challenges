#!/bin/bash

set -x

python3 -c 'print("a"*64)' | python3 chall.py
python3 -c 'print(" "*64)' | python3 chall.py
python3 -c 'print("flag" + "a"*60)' | python3 chall.py
cat flag.txt | python3 chall.py
