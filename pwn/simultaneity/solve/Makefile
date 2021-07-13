.PHONY: default
default: simultaneity

.PHONY: chall
chall:
	$(MAKE) -C ../chall

simultaneity: chall
	@cp ../chall/$@ ../chall/lib/libc.so.6 ./
	patchelf \
		--set-interpreter \
			$(realpath $(shell pwd)/../chall/lib/ld-linux-x86-64.so.2) \
		--set-rpath . \
		$@
