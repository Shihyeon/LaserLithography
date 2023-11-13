import serial
import yaml
import time

class ArduinoLaserControl:
    def __init__(self, port='COM3', baudrate=9600):
        
        with open(file="src\\config.yml", mode="r") as config_file:
            config = yaml.safe_load(config_file)

        port = config['laser']['setup']['port']
        baudrate = config['laser']['setup']['baudrate']

        try:
            self.arduino = serial.Serial(port=port, baudrate=baudrate)
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
    arduino_port = 'COM3'  # 아두이노가 연결된 포트에 따라 변경해야 합니다.

    led_controller = ArduinoLaserControl(arduino_port)

    # LED를 켜고 끄는 예시
    led_controller.onLaser()
    time.sleep(2)  # LED를 켜두고 2초 대기
    led_controller.offLaser()

    led_controller.close()
