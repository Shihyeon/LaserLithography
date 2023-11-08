from PIL import Image
import torch
import torchvision.transforms as tr
import csv

class ImageProcessor:
    def __init__(self, image_path, output_csv):
        self.image_path = image_path
        self.output_csv = output_csv

    def process_image(self):
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

    def filter_result(self):
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

# 이미지 파일 경로와 출력 CSV 파일 이름을 지정합니다.
image_path = 'C:\\image\\image3.jpg'
output_csv = 'filtered_pixel_rgb_values.csv'

# ImageProcessor 클래스의 인스턴스를 생성하고 이미지 처리를 실행합니다.
image_processor = ImageProcessor(image_path, output_csv)
image_processor.process_image()
image_processor.filter_result()