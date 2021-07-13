TARFLAGS := --numeric-owner --owner=0 --group=0 --sort=name --mtime=1970-01-01T00:00Z --no-xattr $(TARFLAGS)

notes.tar.gz: index.js package.json $(shell git ls-files modules public static)
	tar $(TARFLAGS) --transform='s/^/notes\//' -caf $@ $^
