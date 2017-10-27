#!/usr/bin/env bash
arp -n | grep $1 | awk '{print $1}'