import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem
)
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtCore import Qt, QTimer
from sbuck_style import SBUCKStyle


class PaymentScreen(QWidget):
    def __init__(self, on_timer_callback):
        super().__init__()
        self.setFixedSize(SBUCKStyle.WINDOW_WIDTH, SBUCKStyle.WINDOW_HEIGHT)
        self.setStyleSheet(f"background-color: {SBUCKStyle.COLOR_BG}; color: white;")
        self.on_timer_callback = on_timer_callback

    def calculate_fee(self):
        elapsed = self.now - self.entry_time
        total_minutes = int(elapsed.total_seconds() // 60)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        duration_str = f"{hours}시간 {minutes}분" if hours > 0 else f"{minutes}분"

        if total_minutes <= 30:
            fee = 0
        else:
            charged_minutes = total_minutes - 30
            units = (charged_minutes + 9) // 10
            fee = units * 500

        payment = max(fee - self.discount, 0)
        return duration_str, fee, payment

    def init_ui(self, image_name):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "img/cars", image_name)

        # ───── 차량 이미지 박스 ─────
        car_image = QLabel()
        car_image.setFixedSize(220, 160)
        car_image.setScaledContents(True)
        car_image.setStyleSheet(SBUCKStyle.STYLE_IMAGE_BOX)

        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
        else:
            pixmap = QPixmap(car_image.size())
            pixmap.fill(Qt.darkGray)
        car_image.setPixmap(pixmap)

        # ───── 차량 번호 라벨 강조 ─────
        car_number = QLabel(self.car_number)
        car_number.setFont(QFont("Arial", 20, QFont.Bold))
        car_number.setStyleSheet(SBUCKStyle.STYLE_CAR_NUMBER_LABEL)

        # ───── 이미지 컨테이너 ─────
        image_container = QWidget()
        image_container.setFixedWidth(340)
        image_layout = QVBoxLayout()
        image_layout.setAlignment(Qt.AlignCenter)
        image_layout.setContentsMargins(0, 0, 0, 0)
        image_layout.setSpacing(10)
        image_layout.addWidget(car_image)
        image_layout.addWidget(car_number)
        image_container.setLayout(image_layout)

        # ───── 요금 테이블 ─────
        table = QTableWidget(5, 2)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setVisible(False)
        table.setFixedSize(302, 202)
        table.setColumnWidth(0, 100)
        table.setColumnWidth(1, 200)
        table.setSelectionMode(QTableWidget.NoSelection)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setStyleSheet(SBUCKStyle.PAYMENT_STYLE_TABLE)

        for i in range(5):
            table.setRowHeight(i, 40)

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
            title_item.setFont(SBUCKStyle.FONT_MAIN)
            title_item.setBackground(QColor("#325156"))
            title_item.setForeground(QColor("white"))

            value_item = QTableWidgetItem(value)
            value_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            value_item.setFont(QFont("Arial", 14, QFont.Bold))
            value_item.setBackground(QColor("white"))
            value_item.setForeground(QColor("black"))

            if "할인" in title:
                title_item.setBackground(QColor("#014d97"))
                value_item.setForeground(QColor("#014d97"))
            elif "결제" in title:
                title_item.setBackground(QColor("#b43832"))
                value_item.setForeground(QColor("#b43832"))

            table.setItem(i, 0, title_item)
            table.setItem(i, 1, value_item)

        right_layout = QVBoxLayout()
        right_layout.setSpacing(10)
        right_layout.addWidget(table)

        # ───── 상단 레이아웃 ─────
        top_layout = QHBoxLayout()
        top_layout.setSpacing(30)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.addStretch(1)
        top_layout.addWidget(image_container)
        top_layout.addLayout(right_layout)
        top_layout.addStretch(1)

        # ───── 안내 문구 ─────
        notice = QLabel("할인카드 또는 쿠폰을 접촉하여\n주차 요금을 할인받을 수 있습니다")
        notice.setAlignment(Qt.AlignCenter)
        notice.setFont(QFont("Arial", 12))
        notice.setStyleSheet("margin-top: 20px;")

        # ───── 전체 레이아웃 ─────
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(notice)
        self.setLayout(main_layout)

        QTimer.singleShot(2000, self.on_timer_callback)

    def load_car_data(self, barcode_info, car_number, entry_time_str):
        self.car_number = car_number
        self.entry_time_str = entry_time_str
        self.barcode_info = barcode_info

        discount_amount = int(barcode_info.split('-')[1])
        self.entry_time = datetime.strptime(self.entry_time_str, "%Y-%m-%d %H:%M:%S")
        self.discount = discount_amount
        self.now = datetime.now()

        self.duration_str, self.fee, self.payment = self.calculate_fee()
        image_name = f"car_{self.car_number}.png"
        self.init_ui(image_name)


# 테스트 실행
if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = PaymentScreen(lambda: print("다음 화면으로 이동"))
    screen.setWindowTitle("I PARKING - 차량 요금 정산 화면")
    screen.load_car_data(
        barcode_info="2025041224815-5000",
        car_number="112가 4567",
        entry_time_str="2025-04-02 13:00:00",
    )
    screen.show()
    sys.exit(app.exec_())
