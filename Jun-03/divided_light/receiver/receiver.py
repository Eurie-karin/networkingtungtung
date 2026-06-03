import socket
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 9000))
server.listen(5)
print("Receiver listening...", flush=True)

while True:
    conn, addr = server.accept()
    data = conn.recv(1024).decode().strip()
    conn.close()

    if data.startswith("ALERT:"):
        print(f"\n{'='*40}", flush=True)
        print(f"!!! UNKNOWN USER DETECTED !!!", flush=True)
        print(f"{data}", flush=True)
        print(f"{'='*40}\n", flush=True)
        time.sleep(5)  # pause comms for 5 seconds
    else:
        print(data, flush=True)
