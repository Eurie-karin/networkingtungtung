#!/bin/bash

curl -s -X POST http://receiver:8080/notify \
  -H "Content-Type: application/json" \
  -d "{\"user\": \"$USER\", \"time\": \"$(date)\"}"

exec /bin/bash
