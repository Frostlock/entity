#!/usr/bin/env bash
# Query arp cache for IP
# Note that a ping sweep might be helpful to populate the arp cache
arp -n | grep $1 | awk '{print $1}'