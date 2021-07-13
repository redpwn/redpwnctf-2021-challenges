FROM redpwn/jail:v0.0.2

# debian:buster
COPY --from=debian@sha256:5625c115ad881f19967a9b66416f8d40710bb307ad607d037f8ad8289260f75f \
	/ /srv

WORKDIR /srv/app/

COPY chall/flag.txt .
COPY chall/simultaneity run
