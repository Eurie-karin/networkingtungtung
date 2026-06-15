// sketch/blink_serial/blink_serial.ino
// Accepts: "blink <count> <period_ms>\n" over serial

void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    String line = Serial.readStringUntil('\n');
    line.trim();

    if (line.startsWith("blink")) {
      int firstSpace  = line.indexOf(' ');
      int secondSpace = line.indexOf(' ', firstSpace + 1);

      int count  = line.substring(firstSpace + 1, secondSpace).toInt();
      int period = line.substring(secondSpace + 1).toInt();
      int half   = period / 2;

      for (int i = 0; i < count; i++) {
        digitalWrite(LED_BUILTIN, HIGH);
        delay(half);
        digitalWrite(LED_BUILTIN, LOW);
        delay(half);
      }
      Serial.println("done");
    }
  }
}
