import serial
import time

class Laser:
    def __init__(self, port='com3', baud_rate=9600):
        self.arduino = serial.Serial(port, baud_rate)
        time.sleep(1)

    def onLaser(self):
        self.var = '1'.encode('utf-8')
        self.arduino.write(self.var)
        print("Laser turned ON")

    def offLaser(self):
        self.var = '0'.encode('utf-8')
        self.arduino.write(self.var)
        print("Laser turned OFF")

    def controlLaser(self):
        print("'1'을 입력하면 Laser ON & '0'을 입력하면 Laser OFF")
        while True:
            if self.var == '1':
                self.turn_on()
            elif self.var == '0':
                self.turn_off()
            else:
                print("유효한 입력이 아닙니다. '1' 또는 '0'을 입력하세요.")

if __name__ == "__main__":
    laser_controller = Laser()
    laser_controller.controlLaser()
    laser_controller.onLaser()
    time.sleep(5)
    laser_controller.offLaser()