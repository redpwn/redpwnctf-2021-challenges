FROM python:3.9.2-slim-buster

RUN pip install flask gunicorn --no-cache-dir

WORKDIR /app
COPY app.py ./
COPY flag.mp3 ./
COPY static/ ./static/
RUN mkdir /app/db/ && \
    chmod 1773 /app/db/

ENV FLASK_KEY=cc66dec6262b70a5cbc1f17ad3b06dc9

CMD ["gunicorn", "-w4",  "--graceful-timeout", "0", "-unobody", "-gnogroup", "-b0.0.0.0", "app:app"]
