#!/usr/bin/env bash

sender_to_ne_port=4000
ne_network_address=127.0.0.1
recv_recv_port=5000
ne_sender_recv_port=7000
sender_network_address=127.0.0.1
sender_recv_port=8000
max_delay=500
drop_prob=0.5
verbose=$1

python3 ./network_emulator.py $sender_to_ne_port $ne_network_address \
    $recv_recv_port $ne_sender_recv_port $sender_network_address \
    $sender_recv_port $max_delay $drop_prob $verbose
