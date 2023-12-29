#!/bin/sh
ip link set dev eth0 down
ip link set dev eth0 address 06:00:00:00:10:76
ip link set dev eth0 up
