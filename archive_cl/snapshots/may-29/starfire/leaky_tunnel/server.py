#!/usr/bin/env python3
# server.py — TCP bridge to Arduino serial

import socket
import serial
import sys
import time

SERIAL_PORT = "/dev/ttyACM0"   # adjust if yours is /dev/ttyUSB0
BAUD_RATE   = 9600
TCP_HOST    = "0.0.0.0"
TCP_PORT    = 9000


def main():
    print(f"Opening serial port {SERIAL_PORT} at {BAUD_RATE} baud...", flush=True)
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=5)
    except serial.SerialException as e:
        print(f"Could not open serial port: {e}")
        sys.exit(1)

    # Arduino resets when serial opens; give it time to boot
    time.sleep(2)
    print("Serial ready.", flush=True)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((TCP_HOST, TCP_PORT))
        srv.listen(1)
        print(f"Listening on TCP {TCP_HOST}:{TCP_PORT}", flush=True)

        while True:
            conn, addr = srv.accept()
            print(f"Connection from {addr}", flush=True)
            with conn:
                data = conn.recv(1024)
                if not data:
                    continue

                command = data.decode("utf-8").strip()
                print(f"Received: {command!r}", flush=True)

                # Basic validation
                parts = command.split()
                if len(parts) == 3 and parts[0] == "blink":
                    try:
                        count  = int(parts[1])
                        period = int(parts[2])
                        if count < 1 or period < 50:
                            conn.sendall(b"error: count>=1 and period>=50\n")
                            continue
                    except ValueError:
                        conn.sendall(b"error: count and period must be integers\n")
                        continue
                else:
                    conn.sendall(b"error: usage: blink <count> <period_ms>\n")
                    continue

                # Forward to Arduino
                serial_msg = f"{command}\n".encode("utf-8")
                ser.write(serial_msg)
                ser.flush()

                # Wait for Arduino acknowledgement
                response = ser.readline().decode("utf-8").strip()
                print(f"Arduino: {response}", flush=True)
                conn.sendall(f"{response}\n".encode("utf-8"))


if __name__ == "__main__":
    main()
