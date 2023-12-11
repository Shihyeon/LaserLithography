const int Pin = 9;  // 9번 핀을 사용
int brightness = 0;

void setup() {
  pinMode(Pin, OUTPUT);
  analogWrite(Pin, brightness);  // initial brightness
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == '1') {
      brightness = 255;  // minimum 0, maximum 255
      analogWrite(Pin, brightness);  // LED를 켭니다.
      Serial.println("Laser ON");
    } else if (command == '0') {
      brightness = 0;
      analogWrite(Pin, brightness);   // LED를 끕니다.
      Serial.println("Laser OFF");
    }
  }
}
