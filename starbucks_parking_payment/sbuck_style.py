from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QPushButton, QHBoxLayout
import os

class SBUCKStyle:
    # ───────────────────────
    # 폰트 정의
    # ───────────────────────
    FONT_MAIN = QFont("Arial", 12, QFont.Bold)
    FONT_INPUT = QFont("Arial", 18, QFont.Bold)
    FONT_BUTTON = QFont("Arial", 16, QFont.Bold)
    FONT_LABEL = QFont("Arial", 14)

    # ───────────────────────
    # 색상 정의 (문자열 및 QColor)
    # ───────────────────────
    COLOR_BG = "#1E2D3D"
    COLOR_TEXT = "#000000"
    COLOR_TEXT_LIGHT = "#FFFFFF"
    COLOR_CONFIRM = "#134F9E"
    COLOR_CONFIRM_HOVER = "#0F3F80"
    COLOR_CONFIRM_PRESSED = "#0B2B57"
    COLOR_CANCEL = "#D32F2F"
    COLOR_CANCEL_HOVER = "#B71C1C"
    COLOR_CANCEL_PRESSED = "#7F0000"

    # PyQt용 QColor 예시 (필요 시 활용)
    QCOLOR_BG = QColor(COLOR_BG)
    QCOLOR_TEXT = QColor(COLOR_TEXT)

    # ───────────────────────
    # 창 크기
    # ───────────────────────
    WINDOW_WIDTH = 700
    WINDOW_HEIGHT = 400

    # ───────────────────────
    # 경로 정의
    # ───────────────────────
    BASE_PATH = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")

    # ───────────────────────
    # 버튼 스타일
    # ───────────────────────
    STYLE_CONFIRM_BTN = f"""
        QPushButton {{
            background-color: {COLOR_CONFIRM};
            color: {COLOR_TEXT_LIGHT};
            border-radius: 5px;
            padding: 8px 16px;
        }}
        QPushButton:hover {{
            background-color: {COLOR_CONFIRM_HOVER};
        }}
        QPushButton:pressed {{
            background-color: {COLOR_CONFIRM_PRESSED};
        }}
    """

    STYLE_CANCEL_BTN = f"""
        QPushButton {{
            background-color: {COLOR_CANCEL};
            color: {COLOR_TEXT_LIGHT};
            border-radius: 5px;
            padding: 8px 16px;
        }}
        QPushButton:hover {{
            background-color: {COLOR_CANCEL_HOVER};
        }}
        QPushButton:pressed {{
            background-color: {COLOR_CANCEL_PRESSED};
        }}
    """

    STYLE_INPUT = f"""
        QLineEdit {{
            background-color: #FFFFFF;
            color: {COLOR_TEXT};
            border: 2px solid #CCCCCC;
            border-radius: 4px;
            padding: 6px 10px;
        }}
        QLineEdit:focus {{
            border: 2px solid {COLOR_CONFIRM};
        }}
    """

    STYLE_LABEL = f"""
        QLabel {{
            color: {COLOR_TEXT_LIGHT};
            font-size: 14px;
        }}
    """

    # SBUCKStyle에 추가

    STYLE_LABEL_BOLD = """
        QLabel {
            color: #FFFFFF;
            font-family: Arial;
            font-size: 22px;
            font-weight: bold;
        }
    """

    STYLE_TABLE = """
        QTableWidget {
            background-color: #FFFFFF;
            font-size: 14px;
            border: none;
        }
        QTableWidget::item {
            padding: 6px;
        }
        QTableWidget::item:selected {
            background-color: #0078D7;
            color: white;
        }
        QHeaderView::section {
            background-color: #3A4A5B;
            color: white;
            font-weight: bold;
            padding: 6px;
            border: none;
        }
    """

    STYLE_CAR_IMAGE_BOX = """
        QWidget {
            border-image: url(%s);
            background-repeat: no-repeat;
            background-position: center;
            border: 2px solid #496B91;
            border-radius: 10px;
        }
    """

    STYLE_VIDEO_FRAME = """
    QLabel {
        color: #FFFFFF;
        border-radius: 8px;
        border: 3px solid #00704A;
        background-color: #2E3B4E;
    }
    """

    STYLE_BARCODE_INFO = """
        QLabel {
            color: #FFFFFF;
            font-size: 16px;
            font-family: Arial;
            padding: 8px;
        }
    """

    STYLE_LABEL_END = """
    QLabel {
        color: white;
        font-size: 34px;
        font-family: Arial;
        qproperty-alignment: AlignCenter;
    }
    """

    STYLE_EXIT_SCREEN = f"""
        background-color: {COLOR_BG};
    """

    # 차량 이미지 박스
    STYLE_IMAGE_BOX = """
        background-color: #2E3B4E;
        border-radius: 6px;
        padding: 0px;
        margin: 0px;
    """

    # 차량 번호 라벨
    STYLE_CAR_NUMBER_LABEL = """
        background-color: white;
        color: black;
        padding: 10px;
        border-radius: 8px;
        min-width: 200px;
        qproperty-alignment: AlignCenter;
    """

    # 테이블 기본 스타일
    PAYMENT_STYLE_TABLE = """
        border: 1px solid #555;
        font-size: 14px;
    """

    # ───────────────────────
    # 버튼 색상 커스텀 적용 함수
    # ───────────────────────
    @staticmethod
    def get_button_style(color: str):
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border-radius: 5px;
                padding: 8px 16px;
            }}
        """


class HomeButtonLayout(QHBoxLayout):
    def __init__(self, on_button_callback):
        super().__init__()
        self.on_button_callback = on_button_callback

        self.home = QPushButton()
        self.home.setFixedSize(30, 30)
        self.home.setStyleSheet(f"""
        QPushButton {{
            background-color: {SBUCKStyle.COLOR_BG};
            border-image: url({SBUCKStyle.BASE_PATH}/img/icons/home.png);
        }}
        QPushButton:hover {{
            border-image: url({SBUCKStyle.BASE_PATH}/img/icons/home_hover.png);
        }}
        QPushButton:pressed {{
            border-image: url({SBUCKStyle.BASE_PATH}/img/icons/home_hover.png);
        }}
    """)
        self.home.clicked.connect(self.on_button_callback)

        self.addStretch(1)
        self.addSpacing(0)
        self.addWidget(self.home, alignment=Qt.AlignRight)

