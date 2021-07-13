TARFLAGS := --numeric-owner --owner=0 --group=0 --sort=name --mtime=1970-01-01T00:00Z --no-xattr $(TARFLAGS)

lazy-admin.tar.gz: $(shell git ls-files client server)
	tar $(TARFLAGS) --transform='s/^/lazy-admin\//' -caf $@ $^
