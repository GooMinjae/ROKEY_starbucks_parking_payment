import sys 
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem, QAbstractItemView
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import os

from datetime import datetime, timedelta


base_path = os.path.dirname(os.path.realpath(__file__))
base_path = base_path.replace("\\", "/")

class SelectMyCarInfoScreen(QWidget):
    def __init__(self, on_confirm_callback):
        super().__init__()
        self.setWindowTitle("iPARKING - 차량번호 확인")
        # self.setGeometry(300, 300, 800, 400)
        self.setStyleSheet("background-color: #252E3E;")
        self.car_list = []

        layout_space = 20

        self.on_confirm_callback = on_confirm_callback

        # guide label
        guide_label = QLabel()
        guide_label.setText('<span>\
                                고객님 차량을 선택하신 후 <span style="color: #134F9E;">확인</span> 버튼을 눌러주세요\
                            </span>')
        guide_label.setAlignment(Qt.AlignCenter)
        guide_label.setFont(QFont("Arial", 12))
        guide_label.setStyleSheet("color: #FFFFFF;")
        guide_label.setFixedHeight(80)

        # car image widget
        self.car_img_widget = QWidget()
        self.car_img_widget.setFixedSize(250, 250)

        # confirm button
        confirm_btn = QPushButton("확  인")
        confirm_btn.setStyleSheet("""
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
                                """)
        confirm_btn.setFixedSize(250, 50)
        confirm_btn.setFont(QFont("Arial", 15))
        confirm_btn.clicked.connect(self.click_confirm_btn)

        # car list table
        column_title = ["차량번호", "입차시간"]
        self.table_list = QTableWidget()
        self.table_list.setStyleSheet("""
                                        QTableWidget::item {
                                            background-color: #FFFFFF;
                                        }
                                        QTableWidget::item:selected {
                                            background-color: #0078D7;
                                            color: white;
                                        }
                                    """)
        self.table_list.setColumnCount(2)
        self.table_list.setHorizontalHeaderLabels(column_title) # set column title
        self.table_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) # table size stretch
        self.table_list.setSelectionMode(QTableWidget.SingleSelection)
        self.table_list.setSelectionBehavior(QTableWidget.SelectRows) # select entire rows
        self.table_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_list.itemSelectionChanged.connect(self.car_select) # event

        ## layout
        # car image, confirm button layout
        car_img_layout = QVBoxLayout()
        car_img_layout.addWidget(self.car_img_widget)
        car_img_layout.addWidget(confirm_btn)

        # car information layout
        car_info_layout = QHBoxLayout()
        car_info_layout.addSpacing(layout_space) # layout_space = 20
        car_info_layout.addLayout(car_img_layout)
        car_info_layout.addSpacing(layout_space)
        car_info_layout.addWidget(self.table_list)

        # main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(guide_label)
        main_layout.addLayout(car_info_layout)
        main_layout.addSpacing(layout_space)
        self.setLayout(main_layout)

    def load_data(self, car_list):
        self.car_list = car_list
        self.table_list.setRowCount(len(self.car_list))

        for i, value in enumerate(self.car_list):
            self.table_list.setItem(i, 0, QTableWidgetItem(value["번호"]))
            self.table_list.setItem(i, 1, QTableWidgetItem(value["입차시간"]))
        self.table_list.selectRow(0)

    def car_select(self):
        # update selected car data
        self.selected_rows = self.table_list.selectionModel().selectedRows()

        if self.selected_rows:
            row = self.selected_rows[0].row()
            self.car_number = self.table_list.item(row, 0).text()
            self.entry_time = self.table_list.item(row, 1).text()

            # update car image
            car_img = f"{base_path}/img/car_{self.car_number}.png"
            self.car_img_widget.setStyleSheet(f"border-image: url({car_img});\
                                                background-repeat: no-repeat;\
                                                background-position: center;\
                                                margin: 5px")
        else:
            print("선택된 항목이 없습니다.")


    def click_confirm_btn(self):
        if self.selected_rows:
            # print(f"선택된 차량: {self.car_number}, 입차 시간: {self.entry_time}")
            self.on_confirm_callback(self.car_number, self.entry_time)
        else:
            print("선택된 항목이 없습니다.")


if __name__ == "__main__":
    def handle_car_selection(car_number, entry_time):
        print("[콜백 호출됨]")
        print("차량번호:", car_number)
        print("입차시간:", entry_time)

    # 단위 테스트 시 dummy data
    entry_time = datetime.now()

    dummy_data = [
        {"번호": "123가 4567", "입차시간": (entry_time - timedelta(minutes=20)).strftime("%Y-%m-%d %H:%M:%S")},
        {"번호": "245가 4567", "입차시간": (entry_time - timedelta(minutes=80)).strftime("%Y-%m-%d %H:%M:%S")},
        {"번호": "112가 4567", "입차시간": (entry_time - timedelta(minutes=120)).strftime("%Y-%m-%d %H:%M:%S")}
    ]
    app = QApplication(sys.argv)
    win = SelectMyCarInfoScreen(handle_car_selection)
    win.load_data(dummy_data)
    win.show()
    app.exec_()
