import serial
import time
import yaml

class Motor:
    def __init__ (self, port='COM3', baudrate=9600, checkRange=True):
        
        # Open config
        with open(file="scr/config.yml", mode="r") as config_file:
            config = yaml.safe_load(config_file)
        
        # Set port and baudrate value with config
        port = config['Setup']['Port']
        baudrate = config['Setup']['Baudrate']
            
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
                        
        # Set speed value with config
        x_l_speed = config['X_Axis']['L_Speed']
        x_f_speed = config['X_Axis']['F_Speed']
        y_l_speed = config['Y_Axis']['L_Speed']
        y_f_speed = config['Y_Axis']['F_Speed']
        
        # Set rate value with config
        x_rate = config['X_Axis']['Rate']
        x_s_rate = config['X_Axis']['S_Rate']
        y_rate = config['Y_Axis']['Rate']
        y_s_rate = config['Y_Axis']['S_Rate']
        
        # Set initial position value with config
        init_x_pos = config['Initial_Position']['X']
        init_y_pos = config['Initial_Position']['Y']
        
        # axis setting
        x = "1"
        y = "2"
        
        self.setSpeed(x, x_l_speed, x_f_speed)
        self.setSpeed(y, y_l_speed, y_f_speed)
        self.setRate(x, x_rate, x_s_rate)
        self.setRate(y, y_rate, y_s_rate)
        self.goAbs(init_x_pos, init_y_pos)
        
        if checkRange:
            self.goAbs(0, 0)
            self.goAbs(2000, 2000)
            self.goAbs(-2000, -2000)
            self.goAbs(init_x_pos, init_y_pos)

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
        
    def setSpeed(self, axis, lSpeed, fSpeed):
        # set L_Speed
        self.writeCommand(f"axi{axis}:L{axis} {lSpeed}")
        # set F_Speed
        self.writeCommand(f"axi{axis}:F{axis} {fSpeed}")
        
    def setRate(self, axis, Rate, sRate):
        # set Rate
        self.writeCommand(f"axi{axis}:R{axis} {Rate}")
        # set S_Rate
        self.writeCommand(f"axi{axis}:S{axis} {sRate}")
    
    def waitForStop(self):
        while True:
            if self.writeAndGetResponse("MOTIONAll?") == '0':
                break
            time.sleep(0.01)
        time.sleep(0.1)
        
    def close(self):
        self.ser.close()
