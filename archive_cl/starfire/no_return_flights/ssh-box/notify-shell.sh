#!/bin/bash

if [ -t 0 ]; then
    echo "" | nc receiver 9000
    echo "ALERT:user=$USER time=$(date)" | nc receiver 9000
    echo ""
    echo "!!! INTRUSION DETECTED. You have been locked out. !!!"
    echo ""
    exit 1  # closes the connection immediately — no shell given
fi

# Only reaches here if undetected
exec /bin/bash
