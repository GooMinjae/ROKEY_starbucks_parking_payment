import sys
import pyttsx3
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from sbuck_style import SBUCKStyle, HomeButtonLayout

class ExitScreen(QWidget):
    def __init__(self, on_home_btn_callback):
        super().__init__()
        self.on_home_btn_callback = on_home_btn_callback
        self.init_ui()
        self.setFixedSize(SBUCKStyle.WINDOW_WIDTH, SBUCKStyle.WINDOW_HEIGHT)

    def init_ui(self):
        self.setWindowTitle("Exit Screen")
        self.resize(600, 300)
        self.setStyleSheet(SBUCKStyle.STYLE_EXIT_SCREEN)

        # ───── 이미지 로드 ─────
        base_path = SBUCKStyle.BASE_PATH
        image_path = f'{base_path}/img/icons/check_img.png'

        check_img = QLabel()
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path).scaled(150, 150, Qt.KeepAspectRatio)
        else:
            pixmap = QPixmap(150, 150)
            pixmap.fill(Qt.darkGray)

        check_img.setPixmap(pixmap)
        check_img.setAlignment(Qt.AlignCenter)
        home_layout = HomeButtonLayout(self.on_home_btn_callback)

        # ───── 감사 메시지 ─────
        label = QLabel("이용해 주셔서 \n 감사합니다")
        label.setStyleSheet(SBUCKStyle.STYLE_LABEL_END)

        # ───── 레이아웃 ─────
        layout = QVBoxLayout()
        layout.addLayout(home_layout)
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
    window = ExitScreen(lambda: print('home'))
    window.show()
    sys.exit(app.exec_())
