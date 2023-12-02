import serial
import time
from config import Config

# class Laser:
#     def __init__(self, port='COM4', baudrate=9600):
        
#         configInstance = Config()
#         config = configInstance.configuration

#         port = config['laser']['setup']['port']
#         baudrate = config['laser']['setup']['baudrate']

#         try:
#             self.arduino = serial.Serial(port=port, baudrate=baudrate)
#         except Exception as e:
#             raise Exception(f"Usb not connected or port doesn't have permission for serial. try 'sudo chmod 666 {port}'")
        
#         time.sleep(2)

#     def onLaser(self):
#         self.arduino.write(b'1')
#         print("Laser ON")

#     def offLaser(self):
#         self.arduino.write(b'0')
#         print("Laser OFF")

#     def close(self):
#         self.arduino.close()

class Laser:
    def __init__(self, port='COM4', baudrate=9600):
        
        try:
            self.arduino = serial.Serial(port, baudrate)
        except Exception as e:
            raise Exception(f"Usb not connected or port doesn't have permission for serial. try 'sudo chmod 666 {port}'")
        
        time.sleep(2)

    def onLaser(self):
        self.arduino.write(b'1')
        print("Laser ON")

    def offLaser(self):
        self.arduino.write(b'0')
        print("Laser OFF")

    def close(self):
        self.arduino.close()

if __name__ == "__main__":
    laser = Laser()

    # LED를 켜고 끄는 예시
    laser.onLaser()
    time.sleep(5)  # LED를 켜두고 2초 대기
    laser.offLaser()

    laser.close()
