import serial # 아두이노와 통신을 위해 시리얼 통신 설정
import time 

arduino = serial.Serial('com9',9600) 
# com9번이 아두이노에 연결, 보드레이트가 9600(1초에 9600bit)
time.sleep(1)

print ("'1'을 입력하면 LED ON & '0'을 입력하면 LED OFF")

while 1:
    var = input()

    if (var == '1'): # var에 저장된 값이 1
        var = var.encode ('utf-8')
        # var의 값을 'utf-8' 형식으로 인코드해서 var에 저장
        arduino.whrite(var)
        # 인코드된 'var'의 값이 시리얼 통신을 통해 아두이노 프로그램으로 전송
        print ("LED turned ON")
        time.sleep(1)

    if (var == '0'):
        var = var.encode('utf-8')
        arduino.write(var)
        print ("LED tuend OFF")
        time.slepp(1)