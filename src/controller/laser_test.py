import serial
import time

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

    while True:
        timing = input()
        if timing == "":
            laser.offLaser()
            break
        else:
            laser.onLaser()
            time.sleep(float(timing))
            laser.offLaser()
            time.sleep(float(timing))
            
    
    laser.close()
