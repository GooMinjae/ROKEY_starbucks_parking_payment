import os
import sys
from datetime import datetime
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QApplication, QGridLayout
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer
from exit_screen import ExitScreen  # ExitScreen 호출

class PaymentScreen(QWidget):
    def __init__(self, car_number, entry_time_str, discount_amount):
        super().__init__()
        self.setStyleSheet("background-color: #1E2D3D; color: white;")
        # 계산
        self.car_number = car_number
        self.entry_time = datetime.strptime(entry_time_str, "%Y.%m.%d %H:%M:%S")
        self.discount = discount_amount
        self.now = datetime.now()
        self.duration_str, self.fee, self.payment = self.calculate_fee()
        # 이미지 파일명 자동 설정
        image_name = f"car_{car_number}.png"
        self.init_ui(image_name)

    def calculate_fee(self):
        elapsed = self.now - self.entry_time
        total_minutes = int(elapsed.total_seconds() // 60)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        duration_str = f"{hours}시간 {minutes}분" if hours > 0 else f"{minutes}분"
        # 요금 계산
        if total_minutes <= 30:
            fee = 0
        else:
            charged_minutes = total_minutes - 30
            units = (charged_minutes + 9) // 10  # 올림 처리
            fee = units * 500
        payment = max(fee - self.discount, 0)
        return duration_str, fee, payment

    def init_ui(self, image_name):
        # 이미지 경로 설정
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "img", image_name)
        # 차량 이미지 및 번호
        car_image = QLabel()
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path).scaled(200, 150, Qt.KeepAspectRatio)
        else:
            pixmap = QPixmap(200, 150)
            pixmap.fill(Qt.darkGray)
        car_image.setPixmap(pixmap)
        car_number = QLabel(self.car_number)
        car_number.setFont(QFont("Arial", 18, QFont.Bold))
        car_number.setStyleSheet("background-color: white; color: black; padding: 10px;")
        left_layout = QVBoxLayout()
        left_layout.addWidget(car_image, alignment=Qt.AlignCenter)
        left_layout.addWidget(car_number, alignment=Qt.AlignCenter)
        # 정산 정보
        info_grid = QGridLayout()
        labels = [
            ("일차 시각", self.entry_time.strftime("%Y.%m.%d %H:%M:%S")),
            ("주차 시간", self.duration_str),
            ("주차 요금", f"{self.fee:,} 원"),
            ("할인 금액", f"-{self.discount:,} 원"),
            ("결제 금액", f"{self.payment:,} 원")
        ]
        for i, (title, value) in enumerate(labels):
            title_label = QLabel(title)
            value_label = QLabel(value)
            if "할인" in title:
                value_label.setStyleSheet("color: #4DA6FF;")
            elif "결제" in title:
                value_label.setStyleSheet("color: red;")
            title_label.setFont(QFont("Arial", 11))
            value_label.setFont(QFont("Arial", 12, QFont.Bold))
            info_grid.addWidget(title_label, i, 0)
            info_grid.addWidget(value_label, i, 1)
        right_layout = QVBoxLayout()
        right_layout.addLayout(info_grid)
        # 상단 레이아웃
        top_layout = QHBoxLayout()
        top_layout.addLayout(left_layout)
        top_layout.addLayout(right_layout)
        # 하단 안내 문구
        notice = QLabel("할인카드 또는 쿠폰을 접촉하여\n주차 요금을 할인받을 수 있습니다")
        notice.setAlignment(Qt.AlignCenter)
        notice.setFont(QFont("Arial", 11))
        notice.setStyleSheet("margin-top: 20px;")
        # 전체 레이아웃
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(notice)
        self.setLayout(main_layout)



# :돋보기: 테스트 실행
if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = PaymentScreen(
        car_number="112가 4567",
        entry_time_str="2025.04.02 13:00:00",
        discount_amount=3500
    )
    screen.setWindowTitle("I PARKING - 차량 요금 정산 화면")
    screen.resize(600, 300)
    screen.show()

    # 2초 뒤에 ExitScreen으로 넘어가기 위한 타이머 설정
    def show_exit_screen():
        screen.exit_window = ExitScreen()  # ExitScreen 인스턴스 생성
        screen.exit_window.show()
        screen.close()  # PaymentScreen 닫기
    QTimer.singleShot(2000, show_exit_screen)


    sys.exit(app.exec_())