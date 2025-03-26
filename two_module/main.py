import sys
from PyQt5.QtWidgets import *


# class FirstScreen(QWidget):
#     def __init__(self, switch_callback):
#         super().__init__()
#         layout = QVBoxLayout()
#         label = QLabel("여기는 첫 번째 화면입니다.")
#         btn = QPushButton("다음 화면으로")
#         btn.clicked.connect(switch_callback)
#         layout.addWidget(label)
#         layout.addWidget(btn)
#         self.setLayout(layout)

# class SecondScreen(QWidget):
#     def __init__(self):
#         super().__init__()
#         layout = QVBoxLayout()
#         label = QLabel("여기는 두 번째 화면입니다.")
#         layout.addWidget(label)
#         self.setLayout(layout)

# class MainWindow(QStackedWidget):
#     def __init__(self):
#         super().__init__()
#         self.setGeometry(300, 300, 800, 300)
#         self.first = FirstScreen(self.go_to_second)
#         self.second = SecondScreen()
#         self.addWidget(self.first)   # index 0
#         self.addWidget(self.second)  # index 1
#         self.setCurrentIndex(0)
#     def go_to_second(self):
#         self.setCurrentIndex(1)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     main = MainWindow()
#     main.show()
#     sys.exit(app.exec())


## 생성자 이외에 데이터 넘길 수 있는 방법?

class FirstScreen(QWidget):
    def __init__(self, handle_number_input):
        super().__init__()
        self.on_confirm_callback = handle_number_input

        layout = QVBoxLayout()
        label = QLabel("여기는 차량번호 입력 화면입니다.")
        btn = QPushButton("입력 완료 (다음 화면으로 이동)")
        btn.clicked.connect(self.input_number)
        layout.addWidget(label)
        layout.addWidget(btn)
        self.setLayout(layout)
        
    def input_number(self):
        self.on_confirm_callback("4567")

class SecondScreen(QWidget):
    def __init__(self, handle_car_selection):
        super().__init__()
        self.on_car_selected_callback = handle_car_selection

        layout = QVBoxLayout()
        self.label = QLabel("여기는 차량 선택 화면입니다.")
        self.select_btn = QPushButton("차량 선택 완료 (결과 전달)")
        self.select_btn.clicked.connect(self.select_car)
        layout.addWidget(self.label)
        layout.addWidget(self.select_btn)
        self.setLayout(layout)

    def load_data(self, car_list):
        self.label.setText(f"조회된 차량 수: {len(car_list)}대")

    def select_car(self):
        self.on_car_selected_callback("123가 4567", "2025-03-26 10:00:00")

# 메인 윈도우: 화면 전환을 담당하는 QStackedWidget
class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.first = FirstScreen(self.handle_number_input)
        self.second = SecondScreen(self.handle_car_selection)

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

