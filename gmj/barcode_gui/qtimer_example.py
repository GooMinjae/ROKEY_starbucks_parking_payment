import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer

class TimerExample(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QTimer 기본 예제")
        self.setGeometry(100, 100, 300, 150)

        self.counter = 0
        self.label = QLabel("숫자: 0", self)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # QTimer 설정
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_counter)
        self.timer.start(1000)  # 1000ms = 1초마다 실행

    def update_counter(self):
        self.counter += 1
        self.label.setText(f"숫자: {self.counter}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimerExample()
    window.show()
    sys.exit(app.exec_())
