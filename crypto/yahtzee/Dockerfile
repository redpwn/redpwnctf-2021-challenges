FROM python:slim AS app
RUN pip install pycryptodome --no-cache-dir

FROM redpwn/jail:v0.0.2
COPY --from=app / /srv
COPY server.py /srv/app/run

COPY flag.txt /srv/app
COPY quotes.txt /srv/app
COPY keyfile /srv/app

ENV JAIL_MEM=30M JAIL_POW=5000 JAIL_TIME=120
