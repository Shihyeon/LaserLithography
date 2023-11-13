import serial
import time

class LaserController:
    def __init__(self, port='COM7', baud_rate=9600):
        self.arduino = serial.Serial(port, baud_rate)
        time.sleep(1)
        self.laser_on = False  # 초기 상태를 레이저 끈 상태로 설정

    def toggle_laser(self):
        if self.laser_on:
            self.arduino.write('0'.encode('utf-8'))  # 레이저 끄기
            self.laser_on = False
            print("Laser turned OFF")
        else:
            self.arduino.write('1'.encode('utf-8'))  # 레이저 켜기
            self.laser_on = True
            print("Laser turned ON")

if __name__ == "__main__":
    laser_controller = LaserController()

    # 원하는 명령을 호출하여 Laser를 제어
    laser_controller.toggle_laser()  # Laser를 토글하는 명령
    time.sleep(10)  # 일정 시간 대기
    laser_controller.toggle_laser()  # Laser를 다시 토글하는 명령
