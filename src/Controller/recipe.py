from datareader import CSVDataReader
from motor import Motor

class Recipe():
    def __init__(self):
        self.motor = Motor()
        
        # CSVDataReader 클래스의 인스턴스 생성
        self.csv_reader = CSVDataReader(path="src\\resources\\test.csv")
        # CSV 파일 읽기 메서드 호출
        self.csv_reader.read_csv()
        
    def goRecipe(self):
        csv_size = len(self.csv_reader.X)
        for i in range(csv_size):
            self.motor.goAbs(self.csv_reader.X[i], self.csv_reader.Y[i])


if __name__ == "__main__":
    recip = Recipe()

    # X 및 Y 리스트 출력
    print("X:", recip.csv_reader.X)
    print("Y:", recip.csv_reader.Y)
    # csv_size = len(recip.csv_reader.X)
    # for i in range(csv_size):
    #     print(recip.csv_reader.X[i], recip.csv_reader.Y[i])

