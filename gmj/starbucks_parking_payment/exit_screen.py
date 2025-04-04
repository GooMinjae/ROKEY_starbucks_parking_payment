import sys
import pyttsx3
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, QTimer
class ExitScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()


    def init_ui(self):
        self.setWindowTitle("Exit Screen")
        # self.setGeometry(100, 100, 800, 600)
        self.resize(600, 300)
        self.setStyleSheet("background-color: #0E291B;")


        base_path = os.path.dirname(os.path.realpath(__file__))
        base_path = base_path.replace("\\", "/")
        image_path = f'{base_path}/img/icons/check_img.png'

        check_img = QLabel()
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path).scaled(150, 150, Qt.KeepAspectRatio)
        else:
            pixmap = QPixmap(150, 150)
            pixmap.fill(Qt.darkGray)
        check_img.setPixmap(pixmap)
        check_img.setAlignment(Qt.AlignCenter)


        layout = QVBoxLayout()
        label = QLabel("이용해 주셔서 \n 감사합니다")
        label.setFont(QFont("Arial", 34))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: white;")
        layout.addWidget(check_img)
        layout.addWidget(label)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)


    def speak(self):
        engine = pyttsx3.init()
        engine.say("이용해 주셔서 감사합니다.")
        engine.runAndWait()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExitScreen()
    # window.resize(600, 300)
    window.show()
    sys.exit(app.exec_())