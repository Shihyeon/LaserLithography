import yaml
import csv
import serial
import time
import os
import tkinter as tk
import threading
import torch
import torchvision.transforms as tr
from PIL import Image
from loguru import logger
from datetime import datetime


class Config():
    def __init__(self):
        try:
            with open(file="config.yml", mode="r") as config_file:
                self.configuration = yaml.safe_load(config_file)
        except FileNotFoundError:
            print("File not found or path incorrect.")
            self.configuration = {}

class CSVDataReader:
    def __init__(self, path):
        self.file_path = path
        self.X = []
        self.Y = []

    def read_csv(self):
        with open(self.file_path, mode="r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            for row in csv_reader:
                x_value = int(row['X'])
                y_value = int(row['Y'])
                self.X.append(x_value)
                self.Y.append(y_value)

    def close(self):
        # 파일을 열었지만 닫지 않는 것이 좋습니다.
        pass

class Logger:
    def __init__(self, log_dir="log"):
        self.log_dir = log_dir
        self.log_file = self.generateLogFile()
        self.configureLogger()
    
    def generateLogFile(self):
        now = datetime.now()
        formatted_datetime = now.strftime("%Y-%m-%d_%H-%M-%S")
        log_file = os.path.join(self.log_dir, f"Report_{formatted_datetime}.log")
        return log_file
    
    def configureLogger(self):
        logger.remove()  # 기존 핸들러 제거
        logger.add(self.log_file, level="TRACE", format="<green>{time:YYYY-MM-DD HH:mm:ss.SS}</green> | <level>{level: <8}</level> | <level>{message}</level>", rotation="1 week", retention="2 weeks")
    
    def getLogger(self):
        return logger

class ErrorLogger:
    def __init__(self, log_dir="log"):
        self.log_dir = log_dir
        self.error_log_file = self.generateErrorLogFile()
        self.configureErrorLogger()
    
    def generateErrorLogFile(self):
        now = datetime.now()
        formatted_datetime = now.strftime("%Y-%m-%d_%H-%M-%S")
        error_log_file = os.path.join(self.log_dir, f"ErrorReport_{formatted_datetime}.log")
        return error_log_file
    
    def configureErrorLogger(self):
        logger.remove()  # Remove any existing handlers
        logger.add(self.error_log_file, level="ERROR", format="<green>{time:YYYY-MM-DD HH:mm:ss.SS}</green> | <level>{level: <8}</level> | <level>{message}</level>", rotation="1 week", retention="2 weeks")
    
    def getErrorLogger(self):
        return logger

class Motor:
    def __init__(self, port='COM3', baudrate=9600, checkRange=True):
        
        configInstance = Config()
        config = configInstance.configuration

        # Set port and baudrate value with config
        port = str(config['motor']['setup']['port'])
        baudrate = int(config['motor']['setup']['baudrate'])
        check_range = config['motor']['setup']['check_range']
            
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
        x_l_speed = int(config['motor']['x_axis']['l_speed'])
        x_f_speed = int(config['motor']['x_axis']['f_speed'])
        y_l_speed = int(config['motor']['y_axis']['l_speed'])
        y_f_speed = int(config['motor']['y_axis']['f_speed'])
        
        # Set rate value with config
        x_rate = int(config['motor']['x_axis']['rate'])
        x_s_rate = int(config['motor']['x_axis']['s_rate'])
        y_rate = int(config['motor']['y_axis']['rate'])
        y_s_rate = int(config['motor']['y_axis']['s_rate'])
        
        # Set initial position value with config
        self.init_x_pos = int(config['motor']['initial_position']['x'])
        self.init_y_pos = int(config['motor']['initial_position']['y'])
        
        # axis setting
        self.x = "1"
        self.y = "2"
        
        self.setSpeed(self.x, x_l_speed, x_f_speed)
        self.setSpeed(self.y, y_l_speed, y_f_speed)
        self.setRate(self.x, x_rate, x_s_rate)
        self.setRate(self.y, y_rate, y_s_rate)
        self.goAbs(self.init_x_pos, self.init_y_pos)
        
        if checkRange == check_range:
            self.goAbs(0, 0)
            self.goAbs(2000, 2000)
            self.goAbs(-2000, -2000)
            self.goAbs(self.init_x_pos, self.init_y_pos)

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

class Laser:
    def __init__(self, port='COM4', baudrate=9600):
        
        configInstance = Config()
        config = configInstance.configuration

        port = str(config['laser']['setup']['port'])
        baudrate = int(config['laser']['setup']['baudrate'])

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

class ImageConverter:
    def __init__(self, image_path="resources\\input_image.jpg", output_csv="resources\\filtered_pixel_rgb_values.csv"):
        self.image_path = image_path
        self.output_csv = output_csv

    def processImage(self):
        img = Image.open(self.image_path)
        img.thumbnail((1000, 1000))
        transform = tr.Compose([tr.ToTensor()])
        image_tensor = transform(img)
        _, height, width = image_tensor.shape

        csv_rgbdata = 'pixel_rgb_values.csv'

        with open(csv_rgbdata, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Row", "Column", "Red", "Green", "Blue", "Result"])  # 헤더 작성

            for row in range(height):
                for col in range(width):
                    red_value = image_tensor[0, row, col]
                    green_value = image_tensor[1, row, col]
                    blue_value = image_tensor[2, row, col]
                    if red_value <= 0.35 or green_value <= 0.35 or blue_value <= 0.35:
                        writer.writerow([row, col, red_value.item(), green_value.item(), blue_value.item(), 1])
                    else:
                        writer.writerow([row, col, red_value.item(), green_value.item(), blue_value.item(), 0])

    def filterResult(self):
        csv_rgbdata = 'pixel_rgb_values.csv'
        csv_filtered = 'filtered_pixel_rgb_values.csv'

        with open(csv_filtered, mode='w', newline='') as filtered_csv_file:
            writer = csv.writer(filtered_csv_file)
            writer.writerow(["X", "Y"])  # 헤더 작성

            with open(csv_rgbdata, mode='r') as csv_file:
                reader = csv.reader(csv_file)
                next(reader)  # 헤더를 건너뛰기

                for row in reader:
                    if int(row[5]) == 1:
                        writer.writerow([row[1], row[0]])

class Recipe():
    def __init__(self, app):
        self.count = 0
        self.stop_event = threading.Event()
        self.is_running = False  # 작업 실행 여부를 나타내는 플래그
        self.app = app

        self.motor = Motor()
        self.laser = Laser()
        self.logInstance = Logger()
        self.logger = self.logInstance.getLogger()
        configInstance = Config()
        config = configInstance.configuration
        self.delayDuration = float(config['laser']['setup']['delay_duration'])
        
        self.csv_reader = CSVDataReader(path="resources\\filtered_pixel_rgb_values.csv")
        self.csv_reader.read_csv()

    def stopRecipe(self):
        self.stop_event.set()
        self.is_running = False  # 작업이 중지됨을 표시

    def startRecipe(self):
        self.stop_event.clear()
        threading.Thread(target=self.goRecipe).start()  # 새 스레드에서 goRecipe 실행
        self.is_running = True  # 작업이 시작됨을 표시

    def isRunning(self):
        return self.is_running

        
    def goRecipe(self):
        self.csv_size = len(self.csv_reader.X)
        try:
            for self.count in range(self.csv_size):
                if self.stop_event.is_set():
                    break
                self.target_x = self.motor.init_x_pos + self.csv_reader.X[self.count]
                self.target_y = self.motor.init_y_pos + self.csv_reader.Y[self.count]
                self.motor.goAbs(self.target_x, self.target_y)
                self.laser.onLaser()
                time.sleep(self.delayDuration)
                self.laser.offLaser()
                self.updateCountLabel()
                self.logger.trace(f"Perform lithography at absolute position ({self.target_x}, {self.target_y}).")
        except Exception as e:
            self.logger.error(f"An error occurred in absolute position ({self.target_x}, {self.target_y}).")
            raise Exception(f"An error occurred in absolute position ({self.target_x}, {self.target_y}).")
        else:
            self.logger.success("Success Lithography.")

    def updateCountLabel(self):
        self.app.root.after(0, self.app.updateCountLabel)  # GUI 업데이트 요청

    def startAbs(self, x, y):
        if not self.isRunning():  # 작업이 실행 중이지 않은 경우에만 실행
            self.motor.goAbs(x, y)
            self.is_running = True  # 작업이 시작됨을 표시
            print("Starting Abs")

    def stopAbs(self):
        if self.isRunning():  # 작업이 실행 중인 경우에만 실행
            pass  # 예시로 motor를 중지하는 코드를 추가할 수 있습니다.
            self.is_running = False  # 작업이 중지됨을 표시
            print("Stopping Abs")

class Window:
    def __init__(self, root):
        self.root = root
        self.recipe = Recipe(self)
        self.app = self

        self.LargeFrame = tk.Frame(root)
        self.LargeFrame.pack(anchor="center")
        self.root.title("Laser Lithography")
        
        # Frame1: Title Frame
        self.title_frame = self.setFrame(self.LargeFrame, 0, 0)
        
        self.title1 = self.setTitle(self.title_frame, 0, 0, text="Laser Lithography Control Window")
        
        self.title_empty_10 = self.setEmptyBox(self.title_frame, 1, 0, height=2)
        
        # Frame2: Moving Commands Frame
        self.moving_frame = self.setFrame(self.LargeFrame, 1, 0)
        
        self.moving_subtitle_00 = self.setSubTitle(self.moving_frame, 0, 0, text="< Test moving: Move to Position >", columnspan=5)

        self.moving_empty_10 = tk.Label(self.moving_frame, height=1)
        self.moving_empty_10.grid(row=1, column=0)
        
        self.x_label = tk.Label(self.moving_frame, text="X:", width=2, font=('Arial', 11))
        self.x_label.grid(row=2, column=0)
        self.x_entry = tk.Entry(self.moving_frame, width=10, font=('Arial', 11))
        self.x_entry.grid(row=2, column=1)
        
        self.moving_empty_02 = tk.Label(self.moving_frame, width=2)
        self.moving_empty_02.grid(row=2, column=2)
        
        self.y_label = tk.Label(self.moving_frame, text="Y:", width=2, font=('Arial', 11))
        self.y_label.grid(row=2, column=3)
        self.y_entry = tk.Entry(self.moving_frame, width=10, font=('Arial', 11))
        self.y_entry.grid(row=2, column=4)
        
        self.moving_empty_20 = tk.Label(self.moving_frame, height=1)
        self.moving_empty_20.grid(row=3, column=0)
        
        self.go_abs_button = tk.Button(self.moving_frame, text="Go Absolute", width=26, font=('Arial', 11), command=self.startAbsButton)
        self.go_abs_button.grid(row=4, column=0, columnspan=5)

        self.moving_empty_40 = self.setEmptyBox(self.moving_frame, 5, 0, height=3)
        
        # Frame3: Recipe operating Frame
        self.recipe_frame = self.setFrame(self.LargeFrame, 3, 0)

        self.recipe_subtitle_00 = self.setSubTitle(self.recipe_frame, 0, 0, text="< Recipe operating >", columnspan=5)

        self.recipe_empty_10 = tk.Label(self.recipe_frame, height=1)
        self.recipe_empty_10.grid(row=1, column=0)

        self.scan_count_label = tk.Label(self.recipe_frame, text="- / -", font=('Arial', 12))
        self.scan_count_label.grid(row=2, column=0, columnspan=5)

        self.run_scan_button = tk.Button(self.recipe_frame, text="Run Scanning", width=12, font=('Arial', 11))
        self.run_scan_button.grid(row=3, column=0, columnspan=2)

        self.recipe_empty_32 = tk.Label(self.recipe_frame, width=2)
        self.recipe_empty_32.grid(row=3, column=2)

        self.stop_scan_button = tk.Button(self.recipe_frame, text="Stop Scanning", width=12, font=('Arial', 11))
        self.stop_scan_button.grid(row=3, column=3, columnspan=2)

        self.recipe_empty_40 = tk.Label(self.recipe_frame, height=1)
        self.recipe_empty_40.grid(row=4, column=0)

        self.recipe_count_label = tk.Label(self.recipe_frame, text="- / -", font=('Arial', 12))
        self.recipe_count_label.grid(row=5, column=0, columnspan=5)

        self.run_recipe_button = tk.Button(self.recipe_frame, text="Run Recipe", width=12, font=('Arial', 11), command=self.startRecipeButton)
        self.run_recipe_button.grid(row=6, column=0, columnspan=2)

        self.recipe_empty_62 = tk.Label(self.recipe_frame, width=2)
        self.recipe_empty_62.grid(row=6, column=2)

        self.stop_recipe_button = tk.Button(self.recipe_frame, text="Stop Recipe", width=12, font=('Arial', 11), command=self.stopRecipeButton)
        self.stop_recipe_button.grid(row=6, column=3, columnspan=2)
        
        # Frame4: Exit Frame
        self.exit_frame = self.setFrame(self.LargeFrame, 4, 0)
        
        self.exit_empty_00 = tk.Label(self.exit_frame, height=3)
        self.exit_empty_00.grid(row=0)
        
        self.exit_button = tk.Button(self.exit_frame, text="Exit", width=12, font=('Arial', 11), command=self.closeWindowButton)
        self.exit_button.grid(row=1)
        
        self.exit_empty_20 = tk.Label(self.exit_frame, height=2)
        self.exit_empty_20.grid(row=2)
        
        
    def setFrame(self, root, row, column, rowspan=1, columnspan=1):
        self.frame = tk.Frame(root)
        self.frame.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan)
        return self.frame
        
    def setTitle(self, frame, row, column, text, rowspan=1, columnspan=1, width=30, font=('Arial', 20)):
        self.title_label = tk.Label(frame, text=text, width=width, font=font)
        self.title_label.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan)
        
    def setSubTitle(self, frame, row, column, text, rowspan=1, columnspan=1, bg="#E0E0E0", font=('Arial', 12)):
        self.subtitle_label = tk.Label(frame, text=text, bg=bg, font=font, justify=tk.LEFT, relief="groove")
        self.subtitle_label.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky='w')
        
    def setEmptyBox(self, frame, row, column, width=1, height=1):
        self.emptybox = tk.Label(frame, width=width, height=height)
        self.emptybox.grid(row=row, column=column)
    
    # startAbs
    def startAbsButton(self):
        # Disable command (버튼 커멘드가 실행되는 동안 다른 버튼을 비활성화 상태로 설정)
        self.go_abs_button.config(state=tk.DISABLED)
        self.run_scan_button.config(state=tk.DISABLED)
        self.stop_scan_button.config(state=tk.DISABLED)
        self.run_recipe_button.config(state=tk.DISABLED)
        self.stop_recipe_button.config(state=tk.DISABLED)
        self.exit_button.config(state=tk.DISABLED)

        thread = threading.Thread(target=self.runAbsWithButtonControl)
        thread.start()

    def runAbsWithButtonControl(self):
        try:
            # 좌표 입력 필드에서 값을 가져옴
            x_input = self.x_entry.get()
            y_input = self.y_entry.get()
            
            if not x_input or not y_input:
                self.EnableButtons()
                return  # 입력이 없는 경우 아무 작업도 수행하지 않음
            
            x_pos = int(x_input)
            y_pos = int(y_input)

            self.recipe.startAbs(x_pos, y_pos)
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        
        time.sleep(2)
        self.recipe.stopRecipe()
        self.EnableButtons()

    # startRecipe
    def startRecipeButton(self):
        if not self.recipe.isRunning():  # 작업이 실행 중이지 않은 경우에만 실행
            self.go_abs_button.config(state=tk.DISABLED)
            self.run_scan_button.config(state=tk.DISABLED)
            self.stop_scan_button.config(state=tk.DISABLED)
            self.run_recipe_button.config(state=tk.DISABLED)
            self.exit_button.config(state=tk.DISABLED)

            start_thread = threading.Thread(target=self.runRecipeWithButtonControl)
            start_thread.start()

    def runRecipeWithButtonControl(self):
        self.recipe.startRecipe()
        print("On startRecipeButton")

        # Recipe 작업이 완료될 때까지 대기
        while self.recipe.isRunning():
            time.sleep(0.1)  # 일시적으로 대기, 이 과정을 수정하여 적절한 대기 방법으로 변경할 수 있습니다.

        # Recipe 작업이 끝나면 버튼 활성화
        self.app.root.after(0, self.EnableButtons)

    # stopRecipe
    def stopRecipeButton(self):
        if self.recipe.isRunning():  # 작업이 실행 중인 경우에만 실행
            self.go_abs_button.config(state=tk.DISABLED)
            self.run_scan_button.config(state=tk.DISABLED)
            self.stop_scan_button.config(state=tk.DISABLED)
            self.run_recipe_button.config(state=tk.DISABLED)
            self.stop_recipe_button.config(state=tk.DISABLED)
            self.exit_button.config(state=tk.DISABLED)

            self.recipe.stopRecipe()
            print("On stopRecipeButton")

            # Recipe 작업이 완료될 때까지 대기
            while self.recipe.isRunning():
                time.sleep(0.1)  # 일시적으로 대기, 적절한 대기 방법으로 변경 가능

            self.EnableButtons()

    # TODO: start and stop scanning
    def startScanningButton(self):
        pass

    def stopScanningButton(self):
        pass

    def EnableButtons(self):
        self.go_abs_button.config(state=tk.NORMAL)
        self.run_scan_button.config(state=tk.NORMAL)
        self.stop_scan_button.config(state=tk.NORMAL)
        self.run_recipe_button.config(state=tk.NORMAL)
        self.stop_recipe_button.config(state=tk.NORMAL)
        self.exit_button.config(state=tk.NORMAL)

    def closeWindowButton(self):
        self.root.destroy()

    # TODO: add percentage
    def updateCountLabel(self):
        count_str = str(self.recipe.count).zfill(len(str(self.recipe.csv_size)))
        csv_size_str = str(self.recipe.csv_size)
        formatted_text = f"{count_str} / {csv_size_str}"
        self.recipe_count_label.config(text=formatted_text, justify='center')

    # TODO: scanning count
    def updateScanningCountLabel(self):
        pass