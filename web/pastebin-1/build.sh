#!/bin/sh
docker build -t pastebin-1 -f Dockerfile.builder .
docker create --name pastebin-1 pastebin-1:latest
docker cp pastebin-1:/app/target/release/pastebin-1 .
docker rm pastebin-1
