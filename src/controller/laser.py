import serial
import time

class LaserController:
    def __init__(self, port='COM7', baud_rate=9600):
        self.arduino = serial.Serial(port, baud_rate)
        time.sleep(1)
        self.laserOn = False  # 초기 상태를 레이저 끈 상태로 설정

    def onLaser(self):
        self.arduino.write('1'.encode('utf-8'))  # 레이저 실행 명령
        self.laserOn = True
        print("Laser started")

    def offLaser(self):
        self.arduino.write('0'.encode('utf-8'))  # 레이저 정지 명령
        self.laserOn = False
        print("Laser stopped")

if __name__ == "__main__":
    laserController = LaserController()

    # 레이저 실행 명령
    laserController.onLaser()
    time.sleep(10)  # 일정 시간 대기
    # 레이저 정지 명령
    laserController.offLaser()
