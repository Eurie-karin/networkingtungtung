
FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    curl \
    bash \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --break-system-packages pyserial==3.5

RUN curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh \
    | BINDIR=/usr/local/bin sh

RUN arduino-cli config init

RUN arduino-cli core update-index && \
    arduino-cli core install arduino:avr

WORKDIR /app
COPY requirements.txt .
COPY server.py .
COPY sketch/ ./sketch/

RUN arduino-cli compile --fqbn arduino:avr:mega /app/sketch/blink_serial

EXPOSE 9000

CMD ["bash", "-c", \
    "arduino-cli upload --fqbn arduino:avr:mega --port /dev/ttyACM0 /app/sketch/blink_serial && \
     python3 server.py"]

