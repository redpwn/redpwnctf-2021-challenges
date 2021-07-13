CC ?= gcc
CFLAGS := -std=gnu11 -z now -Wall $(CFLAGS)

.PHONY: default
default: simultaneity

simultaneity: simultaneity.c
	$(CC) $(CFLAGS) -o $@ $^

.PHONY: extract-libs
extract-libs:
	docker run --rm -v $(shell pwd)/lib:/host debian:buster /bin/bash -c 'cp /lib/x86_64-linux-gnu/{libc.so.6,ld-linux-x86-64.so.2} /host; chown $(shell id -u):$(shell id -g) /host/*'
