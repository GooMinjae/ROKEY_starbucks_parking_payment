import sys 
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit, QHBoxLayout,
    QGridLayout, QVBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
from sbuck_style import SBUCKStyle
import os

base_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

class FindMyCarInfoScreen(QWidget):
    def __init__(self, on_confirm_callback):
        super().__init__()
        self.on_confirm_callback = on_confirm_callback
        self.setWindowTitle("iPARKING 주차정산기")
        self.setStyleSheet(f"background-color: {SBUCKStyle.COLOR_BG};")
        self.setFixedSize(SBUCKStyle.WINDOW_WIDTH, SBUCKStyle.WINDOW_HEIGHT)

        btn_size_x, btn_size_y = 70, 70

        # ─────────────────────
        # 안내 라벨
        # ─────────────────────
        guide_label = QLabel()
        guide_label.setText('''
            <span style="color: #FFFFFF; font-family: Arial; font-size: 20px;">
                차량번호 4자리 입력 후<br>
                <span style="color: #496B91;">확인</span> 버튼을 눌러주세요
            </span>
        ''')
        guide_label.setAlignment(Qt.AlignCenter)
        guide_label.setFixedSize(300, 60)

        # ─────────────────────
        # 차량번호 입력칸
        # ─────────────────────
        self.num_field = []
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)
        for _ in range(4):
            field = QLineEdit()
            field.setMaxLength(1)
            field.setAlignment(Qt.AlignCenter)
            field.setFont(SBUCKStyle.FONT_INPUT)
            field.setFixedSize(btn_size_x, btn_size_y)
            field.setReadOnly(True)
            field.setStyleSheet(SBUCKStyle.STYLE_INPUT)
            self.num_field.append(field)
            input_layout.addWidget(field)

        # ─────────────────────
        # 버튼 배열 (간격 조정 포함)
        # ─────────────────────
        dialog_list = [["1", "2", "3"],
                       ["4", "5", "6"],
                       ["7", "8", "9"],
                       ["취소", "0", "확인"]]

        dialog_layout = QGridLayout()
        dialog_layout.setHorizontalSpacing(8)
        dialog_layout.setVerticalSpacing(8)

        for i, row in enumerate(dialog_list):
            for j, dialog_text in enumerate(row):
                btn = QPushButton(dialog_text)
                btn.setFont(SBUCKStyle.FONT_BUTTON)
                btn.setFixedSize(btn_size_x, btn_size_y)

                if dialog_text == "취소":
                    btn.setStyleSheet(SBUCKStyle.STYLE_CANCEL_BTN)
                elif dialog_text == "확인":
                    btn.setStyleSheet(SBUCKStyle.STYLE_CONFIRM_BTN)
                else:
                    btn.setStyleSheet(SBUCKStyle.get_button_style("#3A4A5B"))

                btn.clicked.connect(self.handle_button_click)
                dialog_layout.addWidget(btn, i, j)

        # ─────────────────────
        # 전체 레이아웃
        # ─────────────────────
        left_layout = QVBoxLayout()
        upper_spacer = QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding)
        left_layout.addItem(upper_spacer)
        left_layout.addWidget(guide_label)
        left_layout.addLayout(input_layout)
        left_layout.addStretch(1)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)  # 좌우 위아래 마진
        main_layout.setSpacing(40)  # 입력창과 버튼 간 간격
        main_layout.addLayout(left_layout)
        main_layout.addLayout(dialog_layout)
        self.setLayout(main_layout)

    def handle_button_click(self):
        sender = self.sender()
        text = sender.text()

        if text == "취소":
            for field in self.num_field:
                field.clear()
        elif text == "확인":
            value = "".join(field.text() for field in self.num_field)
            if 0 < len(value) <= 4:
                self.on_confirm_callback(value)
            else:
                print("번호가 입력되지 않았습니다.")
        else:
            for field in self.num_field:
                if field.text() == "":
                    field.setText(text)
                    break

if __name__ == "__main__":
    def handle_number_input(input_number):
        print(f"입력된 차량번호: {input_number}")

    app = QApplication(sys.argv)
    win = FindMyCarInfoScreen(handle_number_input)
    win.show()
    app.exec_()
