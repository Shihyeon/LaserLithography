from PIL import Image
import torchvision.transforms as tr
import torch
import csv

# 이미지 크기에 따라 빈 텐서를 생성
image_size = (1000, 1000)  # 이미지 크기에 따라 업데이트
converted_tensor = torch.zeros(image_size)

# CSV 파일에서 데이터 읽어오기
csv_filename = 'pixel_rgb_values.csv'

with open(csv_filename, mode='r', newline='') as csv_file:
    reader = csv.reader(csv_file)
    header = next(reader)  # 첫 번째 행은 헤더입니다.

    for row in reader:
        row_num = int(row[0])
        col_num = int(row[1])
        result = int(row[5])

        # Result 값을 텐서에 할당
        converted_tensor[row_num, col_num] = result

# 텐서를 PIL 이미지로 변환
converted_image = converted_tensor.unsqueeze(0)  # 2D 텐서를 3D 이미지로 변환
converted_image = converted_image * 255  # 0-1 범위를 0-255 범위로 스케일 조정
converted_image = converted_image.byte()  # 이미지 데이터 타입 변경

# NumPy 배열을 사용하여 PIL 이미지를 생성
converted_image_pil = Image.fromarray(converted_image[0].numpy(), 'L')

# PIL 이미지를 파일로 저장
output_image_filename = 'converted_image.png'
converted_image_pil.save(output_image_filename)