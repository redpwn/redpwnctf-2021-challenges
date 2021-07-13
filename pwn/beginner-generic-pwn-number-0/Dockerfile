FROM redpwn/jail:v0.0.2

COPY --from=ubuntu:20.04 / /srv
COPY bin/beginner-generic-pwn-number-0 /srv/app/run
COPY bin/flag.txt /srv/app/flag.txt
