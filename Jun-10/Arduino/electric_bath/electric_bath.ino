/*
 * divided_light :: morse receiver
 * ════════════════════════════════════════════════════════════════════
 * Receives a space-separated Morse string over Serial at 9600 baud.
 * Blinks the built-in LED (pin 13).
 * Replies "SUCCESS\n" or "FAILURE\n" depending on whether the code
 * matches EXPECTED_MORSE.
 *
 * Morse string format (produced by transmit.py):
 *   Character codes separated by single spaces.
 *   Word boundaries marked with " / ".
 *   Example: "-.. .. / .-.. .."
 *
 * Timing follows ITU-R M.1677 conventions.
 * Adjust UNIT_MS to change the overall transmission speed.
 * ════════════════════════════════════════════════════════════════════
 */

#define LED_PIN  13

// ── Timing ─────────────────────────────────────────────────────────────────────
#define UNIT_MS       120           // one Morse unit in milliseconds
#define DOT_ON        (UNIT_MS)
#define DASH_ON       (UNIT_MS * 3)
#define SYM_GAP       (UNIT_MS)     // between dots/dashes within a char
#define CHAR_EXTRA    (UNIT_MS * 2) // added after SYM_GAP → 3 units between chars
#define WORD_EXTRA    (UNIT_MS * 4) // added after SYM_GAP + CHAR_EXTRA → 7 units between words

// ── Expected Morse ─────────────────────────────────────────────────────────────
// Default answer: "DIVIDED LIGHT"
// To regenerate for a different phrase, run:
//   python3 -c "from transmit import encode; print(encode('YOUR PHRASE HERE'))"
//
const char EXPECTED_MORSE[] = "-.. .. ...- .. -.. . -.. / .-.. .. --. .... -";

// ── Helpers ────────────────────────────────────────────────────────────────────

// Blink a single token: a character code like "-.." or a word separator "/".
void blinkToken(const String &tok) {
    if (tok == String("/")) {
        // word gap: extra delay beyond the char gap already applied
        delay(WORD_EXTRA);
        return;
    }
    for (unsigned int i = 0; i < tok.length(); i++) {
        char c = tok.charAt(i);
        if (c == '.') {
            digitalWrite(LED_PIN, HIGH);
            delay(DOT_ON);
            digitalWrite(LED_PIN, LOW);
            delay(SYM_GAP);
        } else if (c == '-') {
            digitalWrite(LED_PIN, HIGH);
            delay(DASH_ON);
            digitalWrite(LED_PIN, LOW);
            delay(SYM_GAP);
        }
    }
    // character gap (SYM_GAP already elapsed after the last symbol)
    delay(CHAR_EXTRA);
}

// Blink a full Morse string by splitting on spaces into tokens.
void blinkMorse(const String &morse) {
    String tok = "";
    for (unsigned int i = 0; i <= morse.length(); i++) {
        // sentinel: treat end-of-string as a space to flush the last token
        char c = (i < morse.length()) ? morse.charAt(i) : ' ';
        if (c != ' ') {
            tok += c;
        } else if (tok.length() > 0) {
            blinkToken(tok);
            tok = "";
        }
    }
}

// Strip all spaces from a String (for normalised comparison).
String normalise(const String &s) {
    String out = "";
    for (unsigned int i = 0; i < s.length(); i++) {
        if (s.charAt(i) != ' ') out += s.charAt(i);
    }
    return out;
}

// ── Setup ──────────────────────────────────────────────────────────────────────
void setup() {
    Serial.begin(9600);
    pinMode(LED_PIN, OUTPUT);
    digitalWrite(LED_PIN, LOW);

    // Ready indicator: three short blinks
    for (int i = 0; i < 3; i++) {
        digitalWrite(LED_PIN, HIGH); delay(80);
        digitalWrite(LED_PIN, LOW);  delay(100);
    }
    delay(300);
}

// ── Loop ───────────────────────────────────────────────────────────────────────
void loop() {
    if (Serial.available() > 0) {
        String rx = Serial.readStringUntil('\n');
        rx.trim();

        if (rx.length() == 0) return;

        // 1. Blink whatever was received
        blinkMorse(rx);
        delay(500);

        // 2. Compare normalised strings (spaces stripped from both sides)
        bool correct = (normalise(rx) == normalise(String(EXPECTED_MORSE)));

        if (correct) {
            Serial.println("SUCCESS");
            // Victory pattern: V (· · · −)
            blinkToken(String("...-"));
            delay(UNIT_MS * 2);
            blinkToken(String("-"));
        } else {
            Serial.println("FAILURE");
            // Failure pattern: three dashes
            blinkToken(String("-"));
            blinkToken(String("-"));
            blinkToken(String("-"));
        }
    }
}
