int data; // 파이썬의 데이터를 저장하기 위함
const int LED = 9;
int i = 0;
bool laserState = false;

void setup() {
  Serial.begin(9600); // 시리얼 통신 시작, 9600은 통신 속도를 의미함
  pinMode(9, OUTPUT); // 9번 핀을 출력 부품으로 설정
  pinMode(LED, OUTPUT);
  digitalWrite(9, LOW); // 9번 핀에 'LOW' 신호 전달
}

void loop() {
  if (Serial.available() > 0) {
    data = Serial.read();
    
    if (data == '1') {
      laserState = true;
      digitalWrite(9, HIGH); // 레이저를 실행
    }
    
    else if (data == '0') {
      laserState = false;
      digitalWrite(9, LOW); // 레이저를 끔
    }
  }

  if (laserState) {
    for (i = 0; i < 255; i++) {
      analogWrite(LED, i);
      delay(10);
    }
    for (i = 255; i > 0; i--) {
      analogWrite(LED, i);
      delay(10);
    }
  }
}
