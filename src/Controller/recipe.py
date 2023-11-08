import csv

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

# CSVDataReader 클래스의 인스턴스 생성
csv_reader = CSVDataReader(path="src\\resources\\test.csv")

# CSV 파일 읽기 메서드 호출
csv_reader.read_csv()

# X 및 Y 리스트 출력
print("X:", csv_reader.X)
print("Y:", csv_reader.Y)

# 파일을 닫을 필요 없음
