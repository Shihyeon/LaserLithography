from reader import CSVDataReader
from motor import Motor
from laser import Laser
from log import Logger
from config import Config
import time
import threading

class Recipe():
    def __init__(self):
        self.motor = Motor()
        self.laser = Laser()
        self.logInstance = Logger()
        self.logger = self.logInstance.getLogger()
        configInstance = Config()
        config = configInstance.configuration
        self.delayDuration = config['laser']['setting']['delay_duration']
        
        self.csv_reader = CSVDataReader(path="src\\resources\\filtered_pixel_rgb_values.csv")
        self.csv_reader.read_csv()

        self.stop_event = threading.Event()

    def stopRecipe(self):
        self.stop_event.set()
        
    def goRecipe(self):
        csv_size = len(self.csv_reader.X)
        try:
            for i in range(csv_size):
                # Check for stop events in the middle
                if self.stop_event.is_set():
                    self.logger.warning("Recipe execution stopped by user.")
                    break
                target_x = self.motor.init_x_pos + self.csv_reader.X[i]
                target_y = self.motor.init_y_pos + self.csv_reader.Y[i]
                self.motor.goAbs(target_x, target_y)
                self.laser.onLaser()
                time.sleep(self.delayDuration)
                self.laser.offLaser()
                self.logger.trace(f"Perform lithography at absolute position ({target_x}, {target_y}).")
        except Exception as e:
            self.logger.error(f"An error occurred in absolute position ({target_x}, {target_y}).")
            raise Exception(f"An error occurred in absolute position ({target_x}, {target_y}).")
        else:
            self.logger.success("Success Lithography.")



if __name__ == "__main__":
    recipe = Recipe()
    recipe.goRecipe()