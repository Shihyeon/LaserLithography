from reader import CSVDataReader
from motor import Motor

class Recipe():
    def __init__(self):
        self.motor = Motor()
        
        # CSVDataReader 클래스의 인스턴스 생성
        self.csv_reader = CSVDataReader(path="src\\resources\\filtered_pixel_rgb_values.csv")
        # CSV 파일 읽기 메서드 호출
        self.csv_reader.read_csv()
        
    def goRecipe(self):
        csv_size = len(self.csv_reader.X)
        for i in range(csv_size):
            target_x = self.motor.init_x_pos + self.csv_reader.X[i]
            target_y = self.motor.init_y_pos + self.csv_reader.Y[i]
            self.motor.goAbs(target_x, target_y)



if __name__ == "__main__":
    recipe = Recipe()
    recipe.goRecipe()

    # X 및 Y 리스트 출력
    # print("X:", recipe.csv_reader.X)
    # print("Y:", recipe.csv_reader.Y)
    # csv_size = len(recip.csv_reader.X)
    # for i in range(csv_size):
    #     print(recip.csv_reader.X[i], recip.csv_reader.Y[i])

