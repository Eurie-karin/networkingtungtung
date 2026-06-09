import socket
import subprocess
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 9000))
server.listen(5)
print("Receiver listening...", flush=True)

last_all_quiet = 0
QUIET_THRESHOLD = 0.5  # ALL_QUIET must have arrived within last 3 seconds

while True:
    conn, addr = server.accept()
    data = conn.recv(1024).decode().strip()
    conn.close()

    if data == "ALL_QUIET":
        last_all_quiet = time.time()
        print("ALL_QUIET", flush=True)

    elif data.startswith("ALERT:"):
        time_since_quiet = time.time() - last_all_quiet

        if time_since_quiet < QUIET_THRESHOLD:
            print("Signal clear. Standing by.", flush=True)
        else:
            print(f"\n{'='*40}", flush=True)
            print("!!! INTRUSION DETECTED !!!", flush=True)
            print(f"{data}", flush=True)
            print("Terminating session...", flush=True)
            print(f"{'='*40}\n", flush=True)
            subprocess.run(
                ["docker", "exec", "divided_light-ssh-box-1", "pkill", "-u", "4rch1v3"],
                capture_output=True
            )
