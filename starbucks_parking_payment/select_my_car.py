# SelectMyCarInfoScreen
# 다른 시스템, 모듈 연동 고려
# 스스로 더미 데이터 만들어 코드 작성, Unit Test

'''
더 봐야할 것
입차시간 or 차량번호 정렬
차량 번호 임의 지정하여 리스트 뽑아오기
더미 데이터 코드 위치, 알고리즘
'''

import sys 
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QTableWidget, QHeaderView, QTableWidgetItem
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import os

from datetime import datetime, timedelta

    # 차량 데이터 샘플
entry_time = datetime.now()

car_data_list = [
    {"번호": "123가 4567", "입차시간": (entry_time - timedelta(minutes=20)).strftime("%Y-%m-%d %H:%M:%S")},
    {"번호": "245가 4567", "입차시간": (entry_time - timedelta(minutes=80)).strftime("%Y-%m-%d %H:%M:%S")},
    {"번호": "112가 4567", "입차시간": (entry_time - timedelta(minutes=120)).strftime("%Y-%m-%d %H:%M:%S")}
]

base_path = os.path.dirname(os.path.realpath(__file__))
base_path = base_path.replace("\\", "/")

class SelectMyCarInfoScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iPARKING 주차정산기(GooMinjae)")
        self.setGeometry(300, 300, 800, 400)
        self.setStyleSheet("background-color: #252E3E;")

        # guide label
        guide_label = QLabel()
        guide_label.setText('고객님 차량을 선택하신 후 확인 버튼을 눌러주세요')
        guide_label.setAlignment(Qt.AlignCenter)
        guide_label.setFont(QFont("Arial", 12))
        guide_label.setStyleSheet("color: #FFFFFF;")

        # car image widget
        self.img_widget = QWidget()
        self.img_widget.setFixedSize(300, 300)
        # self.img_widget.setStyleSheet("margin: 25px; background-color: #333333;")

        # confirm button
        confirm_btn = QPushButton()
        confirm_btn.setText("확인")
        confirm_btn.setStyleSheet("background-color: #134F9E;\
                                    color: #FFFFFF;\
                                    border-radius: 5px;")
        confirm_btn.setFixedSize(300, 50)
        confirm_btn.clicked.connect(self.click_confirm_btn)

        # car list table
        column_title = ["차량번호", "입차시간"]
        self.tabel_list = QTableWidget()
        self.tabel_list.setStyleSheet("background-color: #FFFFFF")
        self.tabel_list.setColumnCount(2)
        self.tabel_list.setHorizontalHeaderLabels(column_title) # set column title
        self.tabel_list.setRowCount(len(car_data_list))
        self.tabel_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) # table size stretch
        self.tabel_list.setSelectionBehavior(QTableWidget.SelectRows) # select entire rows
        self.tabel_list.itemSelectionChanged.connect(self.car_select) # event

        for i, value in enumerate(car_data_list):
            self.tabel_list.setItem(i, 0, QTableWidgetItem(value["번호"]))
            self.tabel_list.setItem(i, 1, QTableWidgetItem(value["입차시간"]))

        self.tabel_list.selectRow(0)


        ## layout
        # car image, confirm button layout
        car_img_layout = QVBoxLayout()
        car_img_layout.addWidget(self.img_widget)
        car_img_layout.addWidget(confirm_btn)

        # car information layout
        car_info_layout = QHBoxLayout()
        car_info_layout.addLayout(car_img_layout)
        car_info_layout.addWidget(self.tabel_list)

        # main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(guide_label)
        main_layout.addLayout(car_info_layout)
        self.setLayout(main_layout)


    def car_select(self):
        self.selected_rows = self.tabel_list.selectionModel().selectedRows()

        if self.selected_rows:
            row = self.selected_rows[0].row()
            self.car_number = self.tabel_list.item(row, 0).text()
            self.entry_time = self.tabel_list.item(row, 1).text()

            car_img = f"{base_path}/img/car_{self.car_number}.png"

            self.img_widget.setStyleSheet(f"border-image: url({car_img});\
                                        background-repeat: no-repeat;\
                                        background-position: center;\
                                        margin: 25px")
        else:
            print("선택된 항목이 없습니다.")


    def click_confirm_btn(self):
        if self.selected_rows:
            print(f"입차 차량 번호: {self.car_number}, 입차 시간: {self.entry_time}")
        else:
            print("선택된 항목이 없습니다.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SelectMyCarInfoScreen()
    win.show()
    app.exec_()
