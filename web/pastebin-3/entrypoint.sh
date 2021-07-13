#!/usr/bin/env bash

set -e

gunicorn -w4 --graceful-timeout 0 -unobody -gnogroup -b0.0.0.0:8000 --chdir /app app:app &
gunicorn -w4 --graceful-timeout 0 -unobody -gnogroup -b0.0.0.0:3000 --chdir /sandbox app:app &
wait -n
