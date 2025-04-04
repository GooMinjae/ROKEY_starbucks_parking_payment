from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import QSize
import os

class SBUCKStyle:
    # 폰트 정의
    FONT_MAIN = QFont("Arial", 12, QFont.Bold)
    FONT_INPUT = QFont("Arial", 18, QFont.Bold)
    FONT_BUTTON = QFont("Arial", 16, QFont.Bold)

    # 색상 정의
    COLOR_BG = "#1E2D3D"
    COLOR_TEXT = "#000000"
    COLOR_CONFIRM = "blue"
    COLOR_CANCEL = "red"

    # 스타일 정의
    STYLE_CONFIRM_BTN = """
                            QPushButton {
                                background-color: #134F9E;
                                color: #FFFFFF;
                                border-radius: 5;
                            }
                            QPushButton:hover {
                                background-color: #0F3F80;
                            }
                            QPushButton:pressed {
                                background-color: #0B2B57;
                            }
                        """

    # 창 크기
    WINDOW_WIDTH = 700
    WINDOW_HEIGHT = 400

    BASE_PATH = os.path.dirname(os.path.realpath(__file__))
    BASE_PATH = BASE_PATH.replace("\\", "/")

    # 버튼 공통 스타일
    @staticmethod
    def get_button_style(color):
        return f"background-color: {color}; color: white;"
