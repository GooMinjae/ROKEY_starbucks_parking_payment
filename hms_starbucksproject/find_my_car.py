
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QGridLayout, QLabel
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class FindMyCarInfoScreen(QWidget):
    def __init__(self, on_confirm_callback=None):
        super().__init__()
        self.on_confirm_callback = on_confirm_callback

        self.setWindowTitle("iPARKING 주차정산기")
        self.setGeometry(100, 100, 500, 350)
        self.setStyleSheet("background-color: #252E3E;")

        mainLayout = QHBoxLayout()

        # Left input area
        leftLayout = QVBoxLayout()
        leftLayout.setSpacing(10)

        self.label = QLabel(
            "차량번호 4자리 입력 후\n<span style='color: #61A0FF;'>확인</span> 버튼을 눌러주세요!"
        )
        self.label.setTextFormat(Qt.RichText)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 12, QFont.Bold))
        leftLayout.addWidget(self.label)

        self.num_fields = []
        inputGrid = QGridLayout()
        inputGrid.setHorizontalSpacing(5)
        inputGrid.setContentsMargins(0, 0, 0, 0)
        for i in range(4):
            field = QLabel("")
            field.setFont(QFont("Arial", 20, QFont.Bold))
            field.setAlignment(Qt.AlignCenter)
            field.setFixedSize(50, 50)
            field.setStyleSheet("background-color: white; color: black; border: 1px solid #ccc;")
            self.num_fields.append(field)
            inputGrid.addWidget(field, 0, i)
        leftLayout.addLayout(inputGrid)

        # Right keypad area
        rightLayout = QVBoxLayout()
        gridLayout = QGridLayout()
        gridLayout.setHorizontalSpacing(5)
        gridLayout.setVerticalSpacing(5)
        gridLayout.setContentsMargins(0, 0, 0, 0)

        numbers = [str(i) for i in range(1, 10)] + ["취소", "0", "확인"]
        positions = [(i, j) for i in range(4) for j in range(3)]
        self.buttons = {}

        for position, number in zip(positions, numbers):
            btn = QPushButton(number)
            btn.setFont(QFont("Arial", 16, QFont.Bold))
            btn.setFixedSize(70, 55)
            style = "background-color: #444; color: white; border-radius: 6px;"
            if number == "취소":
                style = "background-color: red; color: white;"
            elif number == "확인":
                style = "background-color: blue; color: white;"
            btn.setStyleSheet(style)
            btn.clicked.connect(lambda _, t=number: self.handle_button(t))
            self.buttons[number] = btn
            gridLayout.addWidget(btn, *position)

        rightLayout.addLayout(gridLayout)

        mainLayout.addLayout(leftLayout, 1)
        mainLayout.addLayout(rightLayout, 2)

        self.setLayout(mainLayout)

    def handle_button(self, text):
        if text == "취소":
            for field in self.num_fields:
                field.setText("")
        elif text == "확인":
            number = "".join(field.text() for field in self.num_fields)
            if 0 < len(number) <= 4:
                if self.on_confirm_callback:
                    self.on_confirm_callback(number)
                else:
                    print(f"입력된 차량번호: {number}")
            else:
                self.label.setText("숫자를 입력해 주세요!")
        else:
            for field in self.num_fields:
                if field.text() == "":
                    field.setText(text)
                    break

if __name__ == "__main__":
    def handle_number(number):
        print(f"[확인된 차량번호] {number}")

    app = QApplication(sys.argv)
    win = FindMyCarInfoScreen(handle_number)
    win.show()
    sys.exit(app.exec_())
