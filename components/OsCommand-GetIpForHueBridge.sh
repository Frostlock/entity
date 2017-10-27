#!/usr/bin/env bash
# Use arp-scan to scan for Hue IP
# Note that arp-scan requires sudo privileges
sudo arp-scan 192.168.0.0/24 | grep "Philips Lighting BV" | awk '{print $1}'