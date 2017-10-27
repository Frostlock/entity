#!/usr/bin/env bash
# A ping sweep (goal is to populate the arp table)
# fping allows a faster sweep than the regular system ping
for i in `seq 1 255`; do ping -c1 -w1 192.168.1.$i > /dev/null ; done