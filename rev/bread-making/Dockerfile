FROM redpwn/jail:v0.0.2
COPY --from=debian:buster-slim / /srv

COPY bin/main /srv/app/run
COPY bin/flag.txt /srv/app/
