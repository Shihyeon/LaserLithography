import serial
import time

class Laser():
    def __init__(self, port='COM7', baud_rate=9600):
        self.arduino = serial.Serial(port, baud_rate)
        time.sleep(1)
        self.var = '0'  # 초기 상태를 '0'으로 설정

    def onLaser(self):
        self.var = '1'.encode('utf-8')
        self.arduino.write(self.var)
        print("Laser turned ON")

    def offLaser(self):
        self.var = '0'.encode('utf-8')
        self.arduino.write(self.var)
        print("Laser turned OFF")

if __name__ == "__main__":
    laser_controller = Laser()

    # 원하는 명령을 호출하여 Laser를 제어
    laser_controller.onLaser()  # Laser를 켜는 명령
    time.sleep(10)  # 일정 시간 대기
    laser_controller.offLaser()  # Laser를 끄는 명령
