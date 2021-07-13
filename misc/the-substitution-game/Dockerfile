FROM redpwn/jail:v0.0.2

COPY --from=python:3.9-slim / /srv
COPY chall.py /srv/app/run
RUN sed -i 's/\[REDACTED\]/flag{wtf_tur1n9_c0mpl3t3}/g' /srv/app/run

ENV JAIL_MEM=20M
ENV JAIL_TIME=200
