int data; // 파이썬의 데이터를 저장하기 위함
const int LED=9;
int i = 0;

void setup(){
  Serial.begin(9600); // 시리얼 통신 시작, 9600은 통신 속도를 의미함
  pinMode(9,OUTPUT); // 9번 핀을 출력 부품으로 설정
  pinMode(LED,OUTPUT);
  digitalWrite(9,LOW); // 9번 핀에 'LOW' 신호 전달 
}


void loop()

{
  
  while (Serial.available()) // 데이터 수신 계속 검사
  {
    data=Serial.read(); // data에 저장
  }
  
  if (data=='1')
  {
    for(i=0; i<255; i++) // i가 0에서부터 254까지 i=i+1씩 증가
    {
      digitalWrite(9,HIGH);
      analogWrite(LED,i);
      delay(10);
  
    }
    for(i=255; i>0; i--) // i가 255일 때, i<255를 만족하지 않으므로 거짓이 되어 i=i-1씩 감소
    {
      analogWrite(LED,i);
      delay(10);
    }
  }
  else if (data=='0'){
    digitalWrite (9,LOW);
  }
} 