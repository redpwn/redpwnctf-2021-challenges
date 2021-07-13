#!/usr/bin/env bash

set -e

node client/ &
node server/ &
wait -n
