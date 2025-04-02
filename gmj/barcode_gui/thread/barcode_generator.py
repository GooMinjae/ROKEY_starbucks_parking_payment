import os
import barcode
from barcode.writer import ImageWriter
from datetime import datetime

class BarcodeGenerator:
    def __init__(self, free_amount="500000", directory=None):
        """
        BarcodeGenerator 클래스 초기화
        :param free_amount: 바코드에 포함될 무료 금액 (기본값: 5000)
        :param directory: 바코드를 저장할 디렉토리 (기본값: 현재 파일 기준)
        """
        self.free_amount = free_amount
        self.directory = directory or os.path.dirname(os.path.abspath(__file__))  # 디렉토리 기본값 설정

    def create_bar_code(self):
        """ 날짜, 시간, 무료 금액 정보를 포함한 바코드 생성 """
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        bar_data = f"{now}-{self.free_amount}"

        # 바코드 생성 (Code128 바코드 형식 사용)
        code128 = barcode.get_barcode_class('code128')
        barcode_instance = code128(bar_data, writer=ImageWriter())

        # 저장할 경로 설정
        save_path = os.path.join(self.directory, "bar_codes")
        os.makedirs(save_path, exist_ok=True)  # 폴더가 없으면 생성
        file_path = os.path.join(save_path, "bar_code")  # 파일 경로 설정

        options = {
            'module_width': 0.5,     # 선 굵기 키우기
            'module_height': 30.0,   # 세로 높이 늘리기
            'quiet_zone': 6.5,       # 여백 확보
            'write_text': True       # 아래 텍스트 제거
        }
        barcode_instance.save(file_path, options)  # 바코드 저장

        # barcode_instance.save(file_path)  # 바코드 저장

        print(f"바코드 생성 완료: {file_path}")
        return file_path

# 외부에서 호출 예시
if __name__ == "__main__":
    barcode_generator = BarcodeGenerator(free_amount="500000")  # 원하는 금액으로 초기화
    barcode_generator.create_bar_code()  # 바코드 생성