#!/usr/bin/env bash

ne_hostname=127.0.0.1
ne_port_number=7000
recv_port_number=5000
filename=$1

python3 ./receiver.py $ne_hostname $ne_port_number \
    $recv_port_number $filename
