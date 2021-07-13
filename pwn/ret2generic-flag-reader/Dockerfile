FROM redpwn/jail:v0.0.2

# debian:buster-slim
COPY --from=debian@sha256:0fe071e7b4811869579bef3f308096be22f672aa52f121b62c6c401f18abb97c / /srv

WORKDIR /srv/app/

COPY bin/flag.txt .
COPY bin/ret2generic-flag-reader run
