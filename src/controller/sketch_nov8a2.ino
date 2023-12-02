const int ledPin = 9;  // 9번 핀을 사용

void setup() {
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == '1') {
      digitalWrite(ledPin, HIGH);  // LED를 켭니다.
      Serial.println("Laser ON");
    } else if (command == '0') {
      digitalWrite(ledPin, LOW);   // LED를 끕니다.
      Serial.println("Laser OFF");
    }
  }
}
