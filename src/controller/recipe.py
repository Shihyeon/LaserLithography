from reader import CSVDataReader
from motor import Motor
from laser import ArduinoLaserControl
from log import Logger
import time

class Recipe():
    def __init__(self):
        self.motor = Motor()
        self.laser = ArduinoLaserControl()
        self.logInstance = Logger()
        self.logger = self.logInstance.getLogger()
        
        self.csv_reader = CSVDataReader(path="src\\resources\\filtered_pixel_rgb_values.csv")
        self.csv_reader.read_csv()
        
    def goRecipe(self):
        csv_size = len(self.csv_reader.X)
        for i in range(csv_size):
            target_x = self.motor.init_x_pos + self.csv_reader.X[i]
            target_y = self.motor.init_y_pos + self.csv_reader.Y[i]
            self.motor.goAbs(target_x, target_y)
            self.laser.onLaser()
            time.sleep(0.5)
            self.laser.offLaser()
            self.logger.trace(f"Lithography absolute position ({target_x}, {target_y})")
            if i == csv_size:
                self.logger.success("Success Lithography")



if __name__ == "__main__":
    recipe = Recipe()
    recipe.goRecipe()

    # X 및 Y 리스트 출력
    # print("X:", recipe.csv_reader.X)
    # print("Y:", recipe.csv_reader.Y)
    # csv_size = len(recip.csv_reader.X)
    # for i in range(csv_size):
    #     print(recip.csv_reader.X[i], recip.csv_reader.Y[i])

