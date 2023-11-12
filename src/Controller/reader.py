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