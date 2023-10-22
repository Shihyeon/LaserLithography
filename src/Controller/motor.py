import serial
import time

class Motor:
    def __init__ (self, port='COM3', baudrate=9600, checkRange=True):
        try:
            self.ser = serial.Serial(port=port, baudrate=baudrate, stopbits=1)
        except Exception as e:
            raise Exception(f"Usb not connected or port doesn't have permission for serial. try 'sudo chmod 666 {port}'")
        
        # Check for CW and CCW soft limit status
        cw_soft_limit_status = self.writeAndGetResponse(":CWLSET?")
        ccw_soft_limit_status = self.writeAndGetResponse(":CCWLSET?")
        
        if cw_soft_limit_status == '1':
            raise Exception("CW Soft Limit is enabled.")
        if ccw_soft_limit_status == '1':
            raise Exception("CCW Soft Limit is enabled.")
        
        x_speed = 400
        y_speed = 400
        x_rate = 20
        y_rate = 20
        init_x_pos = 0
        init_y_pos = 0
        
        self.setSpeed(x_speed, y_speed)
        self.setRate(x_rate, y_rate)
        self.goAbs(init_x_pos, init_y_pos)
        
        if checkRange:
            self.goAbs(2000, 2000)
            self.goAbs(-2000, -2000)
            self.goAbs(0, 0)

    def writeCommand(self, command: str):
        command += '\r'
        self.ser.write(command.encode())
    
    def getResponse(self):
        output = self.ser.read_until(b'\r')
        return output.decode()[:-1]
    
    def writeAndGetResponse(self, command: str):
        self.writeCommand(command)
        return self.getResponse()
    
    def goAbsWithOutStop(self, xPos, yPos):
        self.writeCommand(f"axi1:goabs {xPos}")
        self.writeCommand(f"axi2:goabs {yPos}")
    
    def goAbs(self, xPos, yPos):
        self.writeCommand(f"axi1:goabs {xPos}")
        self.writeCommand(f"axi2:goabs {yPos}")
        self.waitForStop()
        
    def setSpeed(self, xSpeed, ySpeed):
        # set L_Speed
        self.writeCommand(f"axi1:L1 {xSpeed}")
        # set F_Speed
        self.writeCommand(f"axi1:F1 {xSpeed}")
        self.writeCommand(f"axi2:L2 {ySpeed}")
        self.writeCommand(f"axi2:F2 {ySpeed}")
        
    def setRate(self, xRate, yRate):
        # set Rate
        self.writeCommand(f"axi1:R1 {xRate}")
        # set S_Rate
        self.writeCommand(f"axi1:S1 {xRate}")
        self.writeCommand(f"axi2:R2 {yRate}")
        self.writeCommand(f"axi2:S2 {yRate}")
    
    def waitForStop(self):
        while True:
            if self.writeAndGetResponse("MOTIONAll?") == '0':
                break
            time.sleep(0.01)
        time.sleep(0.1)
        
    def close(self):
        self.ser.close()
