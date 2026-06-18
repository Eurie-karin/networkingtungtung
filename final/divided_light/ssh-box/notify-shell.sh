#!/bin/bash

if [ -t 0 ]; then
    echo "ALERT:user=$USER time=$(date)" | nc receiver 9000
fi

exec /bin/bash
