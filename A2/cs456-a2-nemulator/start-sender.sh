#!/usr/bin/env bash

ne_hostname=127.0.0.1
ne_port=4000
port=8000
timeout=1000
filename=$1

python3 ./sender.py $ne_hostname $ne_port $port $timeout $filename
