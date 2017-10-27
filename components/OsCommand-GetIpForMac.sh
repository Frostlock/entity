#!/usr/bin/env bash
# Use arp-scan to scan for given MAC address
# Note that arp-scan requires sudo privileges
sudo arp-scan 192.168.0.0/24 | grep $1 | awk '{print $1}'