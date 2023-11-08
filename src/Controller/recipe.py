from datareader import CSVDataReader

# CSVDataReader 클래스의 인스턴스 생성
csv_reader = CSVDataReader(path="src\\resources\\test.csv")

# CSV 파일 읽기 메서드 호출
csv_reader.read_csv()

# X 및 Y 리스트 출력
print("X:", csv_reader.X)
print("Y:", csv_reader.Y)

# 파일을 닫을 필요 없음
