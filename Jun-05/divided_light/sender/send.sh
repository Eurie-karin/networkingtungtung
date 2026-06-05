#!/bin/sh
while true; do
    echo "ALL_QUIET" | nc receiver 9000
    sleep 10
done
