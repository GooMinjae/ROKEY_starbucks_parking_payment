from find_my_car import FindMyCarInfoScreen
from select_my_car import SelectMyCarInfoScreen
from barcode_scanner_screen import BarcodeScannerApp
from payment_screen import PaymentScreen
from exit_screen import ExitScreen
from sbuck_style import SBUCKStyle

import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QStackedWidget
from PyQt5.QtGui import QIcon
from datetime import datetime, timedelta

# 메인 윈도우: 화면 전환을 담당하는 QStackedWidget
class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(SBUCKStyle.WINDOW_WIDTH, SBUCKStyle.WINDOW_HEIGHT)  # 메인 고정
        self.setStyleSheet(f"background-color: {SBUCKStyle.COLOR_BG};")
        self.setWindowIcon(QIcon(f"{SBUCKStyle.BASE_PATH}/img/icons/logo.png"))

        self.find_car = FindMyCarInfoScreen(self.handle_number_input)
        self.select_car = SelectMyCarInfoScreen(self.handle_car_selection, self.handle_home_button)
        self.barcode_screen = BarcodeScannerApp(self.handle_detected_barcode, self.handle_home_button)
        self.payment = PaymentScreen(self.handle_timer, self.handle_home_button)
        self.final = ExitScreen(self.handle_home_button)

        self.addWidget(self.find_car)
        self.addWidget(self.select_car)
        self.addWidget(self.barcode_screen)
        self.addWidget(self.payment)
        self.addWidget(self.final)

        self.setCurrentIndex(0)

    def handle_number_input(self, number):
        print(f"[입력된 차량번호] {number}")

        entry_time = datetime.now()
        self.dummy_data = [
            {"번호": f"123가 {number}", "입차시간": (entry_time - timedelta(minutes=20)).strftime("%Y-%m-%d %H:%M:%S")},
            {"번호": f"245가 {number}", "입차시간": (entry_time - timedelta(minutes=80)).strftime("%Y-%m-%d %H:%M:%S")},
            {"번호": f"112가 {number}", "입차시간": (entry_time - timedelta(minutes=120)).strftime("%Y-%m-%d %H:%M:%S")}
        ]
        self.select_car.load_data(self.dummy_data)
        self.setCurrentIndex(1)

    def handle_car_selection(self, car_number, entry_time):
        self.car_number = car_number
        self.entry_time = entry_time
        print(f"[선택된 차량] {self.car_number}, 입차시간: {self.entry_time}")
        self.setCurrentIndex(2)
    
    def handle_detected_barcode(self, barcode_info):
        self.payment.load_car_data(barcode_info, self.car_number, self.entry_time)
        self.setCurrentIndex(3)

    def handle_timer(self):
        self.setCurrentIndex(4)
        QTimer.singleShot(100, self.final.speak)  # 0.1초 후 TTS 실행

    def handle_home_button(self):
        self.find_car.reset()
        self.barcode_screen.close_app()
        self.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("iPARKING")
    window.setStyleSheet(f"background-color: {SBUCKStyle.COLOR_BG}")
    window.resize(600, 500)
    window.show()
    # sys.exit(app.exec())
    app.exec_()
    window.barcode_screen.close_app()

