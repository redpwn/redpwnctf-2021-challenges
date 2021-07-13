TARFLAGS := --numeric-owner --owner=0 --group=0 --sort=name --mtime=1970-01-01T00:00Z --no-xattr $(TARFLAGS)

mdbin.tar.gz: $(shell git ls-files source)
	tar $(TARFLAGS) --transform='s/^source/mdbin/' -caf $@ $^
