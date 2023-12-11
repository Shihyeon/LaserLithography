const int Pin = 9;  // 9번 핀을 사용

void setup() {
  pinMode(Pin, OUTPUT);
  analogWrite(ledPin, 0);  // initial brightness
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    int brightness = Serial.parseInt();

    if (brightness >= 0 && brightness <= 255) {
      analogWrite(ledPin, brightness);
      Serial.println("Brightness set to: " + String(brightness));
    }
  }
}
