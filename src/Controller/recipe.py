import csv

X, Y = [], []
with open(file="src\\resources\\test.csv", mode="r") as csv_file:
    csv_reader = csv.DictReader(csv_file)

    
    # 각 행을 읽어와서 리스트에 추가
    for row in csv_reader:
        x_value = int(row['X'])
        y_value = int(row['Y'])
        X.append(x_value)
        Y.append(y_value)

csv_reader.close()