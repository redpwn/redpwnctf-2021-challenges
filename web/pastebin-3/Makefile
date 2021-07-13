TARFLAGS := --numeric-owner --owner=0 --group=0 --sort=name --mtime=1970-01-01T00:00Z --no-xattr $(TARFLAGS)

pastebin-3.tar.gz: $(shell git ls-files app db sandbox)
	tar $(TARFLAGS) --transform='s/^/pastebin-3\//' -caf $@ $^
