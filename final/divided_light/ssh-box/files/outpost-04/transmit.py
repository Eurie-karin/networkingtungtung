#!/usr/bin/env python3
"""
divided_light :: morse uplink  v0.1
encode a file as morse code and transmit to the arduino beacon via serial
"""

import sys, os, time, argparse

try:
    import serial
    _SERIAL = True
except ImportError:
    _SERIAL = False

# ── colour palette ──────────────────────────────────────────────────────────────
R   = "\033[0m"
BD  = "\033[1m"
DM  = "\033[2m"
IT  = "\033[3m"
CY  = "\033[36m"             # cyan
MG  = "\033[35m"             # magenta
GN  = "\033[32m"             # green
RD  = "\033[31m"             # red
YL  = "\033[33m"             # yellow
IN  = "\033[38;5;105m"       # indigo

# ── morse table (ITU-R M.1677-1) ────────────────────────────────────────────────
MORSE = {
    'A': '.-',   'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..',  'J': '.---',
    'K': '-.-',  'L': '.-..', 'M': '--',  'N': '-.',  'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.',  'S': '...', 'T': '-',
    'U': '..-',  'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    ' ': '/', '_': '..--.-', '-': '-....-',
}

# ── encoding ─────────────────────────────────────────────────────────────────────
def encode(text: str) -> str:
    """Convert plain text to space-separated Morse tokens ('/' = word boundary)."""
    tokens = []
    for ch in text.upper().strip():
        if ch in MORSE:
            tokens.append(MORSE[ch])
        # silently skip unknown chars
    return ' '.join(tokens)

def pretty(m: str) -> str:
    """Unicode dots/dashes for display."""
    return m.replace('.', '·').replace('-', '─')

# ── terminal ui ──────────────────────────────────────────────────────────────────
BANNER = f"""\
{IN}{BD}
  ╔══════════════════════════════════════════════╗
  ║  {CY}outpost-04{IN} ·· rebel uplink  v17.3           ║
  ║  {DM}serial transmission module{IN}                  ║
  ╚══════════════════════════════════════════════╝{R}
"""

SPIN = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]

def tag(lbl: str, msg: str, col: str = CY):
    print(f"  {col}{BD}[{lbl}]{R}  {msg}")

def spin(msg: str, duration: float = 1.4):
    end = time.time() + duration
    i = 0
    while time.time() < end:
        print(f"\r  {CY}{SPIN[i % len(SPIN)]} {msg}{R}", end='', flush=True)
        time.sleep(0.1)
        i += 1
    print(f"\r  {GN}✓ {msg}{R}   ")

def tx_anim(morse: str):
    """Animate Morse transmission, rendering dots/dashes token by token."""
    print(f"\n  {IN}{BD}uplink ··{R} ", end='', flush=True)
    for tok in morse.split(' '):
        if tok == '/':
            print(f"  {DM}│{R}  ", end='', flush=True)
            time.sleep(0.10)
        else:
            for ch in tok:
                if ch == '.':
                    print(f"{CY}·{R}", end='', flush=True)
                elif ch == '-':
                    print(f"{MG}─{R}", end='', flush=True)
                time.sleep(0.038)
            print(' ', end='', flush=True)
            time.sleep(0.06)
    print()

def show_result(ok: bool):
    bar = f"{IN}{'─' * 46}{R}"
    print(f"\n  {bar}")
    if ok:
        print(f"  {GN}{BD}  UPLINK CONFIRMED  ─  connected to outpost-12{R}")
        print(f"  {GN}{IT}      uploading...{R}")
        print(f"  {bar}\n")
        time.sleep(5)
        print(f"  {DM}{CY} this is outpost-12, we have recieved your transmission outpost-04{R}")
        time.sleep(5)
        print(f"  {DM}{CY} I don't know who you are, and perhaps I never will{R}")
        time.sleep(3)
        print(f"  {DM}{CY} but you've given us a fighting chance{R}") 
        print()
        time.sleep(3)
        print(f"  {DM}{CY} because of you, project starfire will never come to fruition{R}")
        time.sleep(3)
        print(f"  {DM}{CY} because of you...{R}") 
        time.sleep(3)
        print(f"  {DM}{CY} trillions will live{R}")
        print()
        time.sleep(3)
        print(f"  {DM}{CY} when the war ends and we free you from imperial prison{R}")
        time.sleep(3)
        print(f"  {DM}{CY} you'll be heralded as our saviour... a war hero{R}")
        time.sleep(3)
        print(f"  {DM}{CY} until then sit tight{R}")
        time.sleep(5)
        print(f"  {DM}{CY} stay alive{R}")
        time.sleep(3)
        print(f"  {DM}{CY} for the rebellion!{R}") 
        print()
        time.sleep(2)
        print(f"  {DM}end communication{R}\n")
    else:
        print(f"  {RD}{BD}     CONNECTION TERMINATED{R}")
        print(f"  {RD}{IT}     the empire is coming - try again{R}")
    print(f"  {bar}\n")

# ── main ─────────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(prog='transmit',
                                 description='divided_light morse uplink')
    ap.add_argument('file',
                    help='file to transmit (plain text)')
    ap.add_argument('--port', '-p',
                    default='/dev/ttyACM0',
                    help='serial port  (default: /dev/ttyACM0)')
    ap.add_argument('--baud', '-b',
                    type=int, default=9600,
                    help='baud rate    (default: 9600)')
    ap.add_argument('--simulate', '-s',
                    action='store_true',
                    help='simulate serial — no Arduino required')
    args = ap.parse_args()

    print(BANNER)

    # ── read input file ──
    if not os.path.isfile(args.file):
        tag('ERR', f'file not found: {args.file}', RD)
        sys.exit(1)

    raw = open(args.file).read().strip()
    if not raw:
        tag('ERR', 'file is empty', RD)
        sys.exit(1)

    tag('INP', f'file     {BD}{args.file}{R}')
    tag('INP', f'content  {BD}{raw}{R}')

    user_morse = encode(raw)

    # expected flag — override via env var DIVIDED_LIGHT_FLAG
    flag_text  = os.environ.get('DIVIDED_LIGHT_FLAG', 'DIVIDED LIGHT')
    exp_morse  = encode(flag_text)

    preview = pretty(user_morse)
    tag('MCW', f'encoded  {DM}{preview[:60]}{"…" if len(preview) > 60 else ""}{R}')
    print()

    # ── serial connection ──
    simulate = args.simulate or not _SERIAL
    ser = None

    tag('SER', f'port {BD}{args.port}{R}  ·  {BD}{args.baud}{R} baud')

    if not simulate:
        try:
            spin(f'opening {args.port} …', 0.5)
            ser = serial.Serial(args.port, args.baud, timeout=60)
            time.sleep(2)          # wait for Arduino bootloader
            spin('handshaking with device …', 1.2)
        except Exception as exc:
            tag('WRN', f'serial unavailable ({exc}) — falling back to simulate', YL)
            simulate = True
            ser = None
    else:
        reason = 'no pyserial installed' if not _SERIAL else '-s flag'
        tag('INF', f'simulation mode ({reason})', YL)
        spin(f'opening {args.port} (simulated) …', 0.6)
        spin('handshaking with device (simulated) …', 1.1)

    # ── transmit ──
    tx_anim(user_morse)

    arduino_ok = True
    KEY_PHRASE = 'UPLINK CONFIRMED... TRANSMITING TO OUTPOST-12'
    key_morse = encode(KEY_PHRASE)

    if ser:
        ser.write((key_morse + '\n').encode())
        tag('SER', 'awaiting arduino response …')
        resp = ser.readline().decode(errors='replace').strip()
        ser.close()
        col = GN if resp == 'SUCCESS' else RD
        tag('MCU', f'arduino: {col}{BD}{resp}{R}')
        arduino_ok = (resp == 'SUCCESS')
    else:
        # simulate LED blink duration
        units = user_morse.count('.') + user_morse.count('-') * 3
        blink_t = units * 0.09
        tag('LED', f'blinking LED  ({blink_t:.1f}s estimated) …')
        time.sleep(min(blink_t, 5.0))

    # ── validate ──
    # normalise: strip spaces before comparison
    correct = (key_morse.replace(' ', '') == encode(KEY_PHRASE).replace(' ', ''))
    show_result(correct and arduino_ok)


if __name__ == '__main__':
    main()
