# 과제
# 번호판 화면 / 기능 정의서
# 정의 서류 온전히 준수 

import sys 
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QHBoxLayout, QGridLayout, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import os

base_path = os.path.dirname(os.path.realpath(__file__))
base_path = base_path.replace("\\", "/")

class FindMyCarInfoScreen(QWidget):
    def __init__(self, on_confirm_callback):
        super().__init__()
        self.on_confirm_callback = on_confirm_callback
        self.setWindowTitle("iPARKING 주차정산기(GooMinjae)")
        self.setGeometry(300, 300, 600, 400)
        self.setStyleSheet("background-color: #252E3E;")

        btn_size_x, btn_size_y = 70, 70

        # guide label
        guide_label = QLabel()
        guide_label.setText('<span style="color: #FFFFFF; font-family: Arial, sans-serif; font-size: 25px;">\
                                차량번호 4자리 입력 후<br><span style="color: #496B91;">확인</span> 버튼을 눌러주세요\
                            </span>')
        guide_label.setAlignment(Qt.AlignCenter)
        guide_label.setFixedSize(300, 60)

        # num text field
        self.num_field = []
        input_layout = QHBoxLayout()
        
        for _ in range(4):
            field = QLineEdit()
            field.setMaxLength(1)
            field.setAlignment(Qt.AlignCenter)
            field.setFont(QFont("Arial", 24))
            field.setFixedSize(btn_size_x, btn_size_y)
            field.setReadOnly(True)
            field.setStyleSheet("background-color: #FFFFFF;")
            self.num_field.append(field)
            input_layout.addWidget(field)

        # dialog buttons
        dialog_list =  [["1", "2", "3"], 
                        ["4", "5", "6"], 
                        ["7", "8", "9"], 
                        ["취소", "0", "확인"]]

        dialog_layout = QGridLayout()
        i, j = 0, 0
        for row in dialog_list:
            for dialog_text in row:
                btn = QPushButton(dialog_text)
                btn.clicked.connect(self.handle_button_click)
                btn.setStyleSheet("background-color: #252E3E;\
                                    color: #FFFFFF;")
                btn.setFixedSize(btn_size_x, btn_size_y)
                btn.setFont(QFont("Arial", 17))

                if dialog_text == "취소":
                    btn.setStyleSheet("background-color: #FF0000;\
                                        color: #FFFFFF;")
                    btn.setFont(QFont("Arial", 12))
                elif dialog_text == "확인":
                    btn.setStyleSheet("background-color: #0000FF;\
                                        color: #FFFFFF;")
                    btn.setFont(QFont("Arial", 12))
                dialog_layout.addWidget(btn, i, j)
                j += 1
            i += 1
            j = 0


        ## layout
        # left text label, number field layout
        left_layout = QVBoxLayout()
        upper_spacer = QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding)
        left_layout.addItem(upper_spacer)
        left_layout.addWidget(guide_label)
        left_layout.addLayout(input_layout)
        left_layout.addStretch(1)

        main_layout = QHBoxLayout()
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
                # print(f"입력된 차량 번호: {value}")
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
