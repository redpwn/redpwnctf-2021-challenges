NAME := chall
CC ?= gcc
CFLAGS := -std=c11 -Wall -Wextra -O3 $(CFLAGS)
LDFLAGS := -Wl,-s $(LDFLAGS)

HEADERS = chall.h

default: $(NAME)

test: chall chall.o

chall.o: chall.c $(HEADERS)
	$(CC) $(CFLAGS) -c -o $@ $<

chall: chall.o
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^
