from src.scanner.converter import ImageProcessor

if __name__ == "__main__":
    # 이미지 파일 경로와 출력 CSV 파일 이름을 지정합니다.
    image_path = 'resources\\input_image.jpg'
    output_csv = 'resources\\filtered_pixel_rgb_values.csv'

    # ImageProcessor 클래스의 인스턴스를 생성하고 이미지 처리를 실행합니다.
    image_processor = ImageProcessor(image_path, output_csv)
    image_processor.process_image()
    image_processor.filter_result()