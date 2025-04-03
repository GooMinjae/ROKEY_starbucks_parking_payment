import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtCore import Qt, QTimer
from exit_screen import ExitScreen  # ExitScreen 호출

class PaymentScreen(QWidget):
    def __init__(self, car_number, entry_time_str, discount_amount):
        super().__init__()
        self.setStyleSheet("background-color: #1E2D3D; color: white;")
        
        # 차량 정보
        self.car_number = car_number
        self.entry_time = datetime.strptime(entry_time_str, "%Y.%m.%d %H:%M:%S")
        self.discount = discount_amount
        self.now = datetime.now()
        
        # 요금 계산
        self.duration_str, self.fee, self.payment = self.calculate_fee()
        
        # 차량 이미지 파일명 설정
        image_name = f"car_{car_number}.png"
        self.init_ui(image_name)
    
    def calculate_fee(self):
        """주차 요금 계산"""
        elapsed = self.now - self.entry_time
        total_minutes = int(elapsed.total_seconds() // 60)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        duration_str = f"{hours}시간 {minutes}분" if hours > 0 else f"{minutes}분"

        # 요금 정책
        if total_minutes <= 30:
            fee = 0
        else:
            charged_minutes = total_minutes - 30
            units = (charged_minutes + 9) // 10  # 10분 단위 올림
            fee = units * 500
        
        payment = max(fee - self.discount, 0)
        return duration_str, fee, payment

    def init_ui(self, image_name):
        """UI 초기화"""
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
        car_number.setStyleSheet("background-color: white; color: black; padding: 8px; border-radius: 5px;")

        left_layout = QVBoxLayout()
        left_layout.addWidget(car_image, alignment=Qt.AlignCenter)
        left_layout.addWidget(car_number, alignment=Qt.AlignCenter)

        # 정산 정보 테이블
        table = QTableWidget(5, 2)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setVisible(False)
        table.setFixedSize(302, 202)
        table.setColumnWidth(0, 100)
        table.setColumnWidth(1, 200)
        table.setSelectionMode(QTableWidget.NoSelection)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setStyleSheet("border: 1px solid #555; font-size: 14px;")

        for i in range(5):
            table.setRowHeight(i, 40)

        # 테이블 데이터 입력
        labels = [
            ("입차 시각", self.entry_time.strftime("%Y.%m.%d %H:%M:%S")),
            ("주차 시간", self.duration_str),
            ("주차 요금", f"{self.fee:,} 원"),
            ("할인 금액", f"-{self.discount:,} 원"),
            ("결제 금액", f"{self.payment:,} 원")
        ]

        for i, (title, value) in enumerate(labels):
            title_item = QTableWidgetItem(title)
            title_item.setTextAlignment(Qt.AlignCenter)
            title_item.setFont(QFont("Arial", 12, QFont.Bold))
            title_item.setBackground(QColor("#325156"))
            title_item.setForeground(QColor("white"))

            value_item = QTableWidgetItem(value)
            value_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            value_item.setFont(QFont("Arial", 14, QFont.Bold))
            value_item.setBackground(QColor("white"))
            value_item.setForeground(QColor("black"))

            # 할인 및 결제 금액 배경색 변경
            if "할인" in title:
                title_item.setBackground(QColor("#014d97"))
                value_item.setForeground(QColor("#014d97"))
            elif "결제" in title:
                title_item.setBackground(QColor("#b43832"))
                value_item.setForeground(QColor("#b43832"))

            table.setItem(i, 0, title_item)
            table.setItem(i, 1, value_item)

        right_layout = QVBoxLayout()
        right_layout.addWidget(table)

        # 상단 레이아웃
        top_layout = QHBoxLayout()
        top_layout.addLayout(left_layout)
        top_layout.addLayout(right_layout)

        # 안내 문구
        notice = QLabel("할인카드 또는 쿠폰을 접촉하여\n주차 요금을 할인받을 수 있습니다")
        notice.setAlignment(Qt.AlignCenter)
        notice.setFont(QFont("Arial", 12))
        notice.setStyleSheet("margin-top: 20px;")

        # 전체 레이아웃
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(notice)
        self.setLayout(main_layout)

        # 2초 후 ExitScreen으로 이동
        # QTimer.singleShot(2000, self.show_exit_screen)

    def show_exit_screen(self):
        """ExitScreen으로 전환"""
        self.exit_window = ExitScreen()
        self.exit_window.show()
        self.close()

# 실행 테스트
if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = PaymentScreen(
        car_number="112가 4567",
        entry_time_str="2025.04.02 13:00:00",
        discount_amount=3500
    )
    screen.setWindowTitle("I PARKING - 차량 요금 정산 화면")
    screen.resize(700, 350)
    screen.show()
    sys.exit(app.exec_())