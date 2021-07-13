FROM python:3.9.2-slim-buster

RUN pip install flask gunicorn --no-cache-dir

WORKDIR /app
COPY app/app.py ./
COPY app/static/ ./static/
COPY app/templates/ ./templates/

WORKDIR /sandbox
COPY sandbox/app.py ./
COPY sandbox/static/ ./static/

RUN mkdir /db/ && \
    chmod 1773 /db/

WORKDIR /
COPY entrypoint.sh ./

ENV FLASK_KEY=f9e288fd610f537d3fb6184ba747c91248aef3bdb0653b3753bcc253da0b3c16
ENV SANDBOX_URL=https://sandbox.pastebin-3.mc.ax
ENV FLAG=flag{c00k13_b0mb1n6_15_f4k3_vuln}

ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--", "/entrypoint.sh"]
