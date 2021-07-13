FROM debian:buster-slim
RUN apt-get update && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY pastebin-1 .
COPY static static
CMD ["./pastebin-1"]
