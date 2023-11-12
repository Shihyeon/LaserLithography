// 파이썬의 데이터를 저장하기 위함
int data; 


void setup(){
  // 시리얼 통신 시작, 9600은 통신 속도를 의미함
  Serial.begin(9600);
  // 13번 핀을 출력 부품으로 설정
  pinMode(13,OUTPUT);
  // 13번 핀에 'LOW' 신호 전달 
  digitalWrite(13,LOW);

}


void loop() {
  // 데이터 수신 계속 검사
  while (Serial.available()) {
  // data에 저장
    data=Serial.read();
  
  }
  
  if (data=='1'){
    digitalWrite(13,HIGH);
  }
  else if (data=='0'){
    digitalWrite (13,LOW);
  }
} 