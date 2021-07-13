TARFLAGS := --numeric-owner --owner=0 --group=0 --sort=name --mtime=1970-01-01T00:00Z --no-xattr $(TARFLAGS)

wtjs.tar: $(shell find src -type f)
	tar $(TARFLAGS) --transform='s/^src/wtjs/' -cf $@ $^
