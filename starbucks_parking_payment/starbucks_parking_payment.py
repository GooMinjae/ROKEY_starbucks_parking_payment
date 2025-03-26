### 시스템의 critical point 판단
from find_my_car import FindMyCarInfoScreen
from select_my_car import SelectMyCarInfoScreen # minseok

import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget

# 메인 윈도우: 화면 전환을 담당하는 QStackedWidget
class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.first = FindMyCarInfoScreen(self.handle_number_input)
        self.second = SelectMyCarInfoScreen(self.handle_car_selection)

        self.addWidget(self.first)   # index 0
        self.addWidget(self.second)  # index 1

        self.setCurrentIndex(0)

    def handle_number_input(self, number):
        print(f"[입력된 차량번호] {number}")

        # 더미 데이터 조회처럼 처리
        dummy_data = [
            {"번호": f"{number}가 1111", "입차시간": "2025-03-26 09:00:00"},
            {"번호": f"{number}가 2222", "입차시간": "2025-03-26 08:45:00"},
        ]
        self.second.load_data(dummy_data)
        self.setCurrentIndex(1)

    def handle_car_selection(self, car_number, entry_time):
        print(f"[선택된 차량] {car_number}, 입차시간: {entry_time}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("QStackedWidget 기본 예제")
    window.resize(600, 300)
    window.show()
    sys.exit(app.exec())

