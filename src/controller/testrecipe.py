from reader import CSVDataReader
from motor import Motor
from laser import Laser
from log import Logger
from config import Config
import time
import threading

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
        self.delayDuration = config['laser']['setup']['delay_duration']
        
        self.csv_reader = CSVDataReader(path="src\\resources\\filtered_pixel_rgb_values.csv")
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


if __name__ == "__main__":
    recipe = Recipe()
    recipe.goRecipe()
