CC ?= gcc
CFLAGS := -std=c11 -Wall -Wextra -O3 $(CFLAGS)
LDFLAGS := -Wl,-s

default: chall genpuzzle prog.bin solve

chall: chall.o
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^


%.o: %.c $(HEADERS)
	$(CC) $(CFLAGS) -c -o $@ $<

%.bin: %.s
	nasm -f bin -o $@ $<

genpuzzle: puzzle.py
	python3 $<

solve: solve.py
	python3 $<
