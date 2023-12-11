import serial
import time
from config import Config

class Laser:
    def __init__(self, port='COM4', baudrate=9600):
        
        try:
            self.arduino = serial.Serial(port, baudrate)
        except Exception as e:
            raise Exception(f"Usb not connected or port doesn't have permission for serial. try 'sudo chmod 666 {port}'")
        
        time.sleep(2)
    
    def setLaserBrightness(self, brightness):
        # 보낼 값을 0에서 255 사이로 제한
        brightness = min(max(brightness, 0), 255)
        self.arduino.write(str(brightness).encode())
        print(f"Brightness set to: {brightness}")

    def close(self):
        self.arduino.close()

if __name__ == "__main__":
    laser = Laser()

    # LED를 켜고 끄는 예시
    laser.setLaserBrightness(255)
    time.sleep(10)  # LED를 켜두고 2초 대기
    laser.setLaserBrightness(0)

    laser.close()
