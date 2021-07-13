FROM redpwn/jail:v0.0.2
COPY --from=gcr.io/distroless/base-debian10 / /srv
COPY flag.txt prog.bin /srv/app/
COPY chall /srv/app/run
