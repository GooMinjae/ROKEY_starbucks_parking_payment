
import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QHeaderView, QAbstractItemView
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from datetime import datetime, timedelta

# 공통 이미지 경로
base_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')

class SelectMyCarInfoScreen(QWidget):
    def __init__(self, on_confirm_callback):
        super().__init__()
        self.setWindowTitle("iPARKING - 차량번호 확인")
        self.setStyleSheet("background-color: #222; color: white;")
        self.on_confirm_callback = on_confirm_callback
        self.car_list = []

        guide_label = QLabel("고객님 차량을 선택하신 후 '확인' 버튼을 눌러주세요.")
        guide_label.setAlignment(Qt.AlignCenter)
        guide_label.setFont(QFont("Arial", 12, QFont.Bold))
        guide_label.setFixedHeight(60)

        self.car_img_widget = QLabel()
        self.car_img_widget.setFixedSize(250, 200)
        self.car_img_widget.setStyleSheet("border: 2px solid white;")

        confirm_btn = QPushButton("확인")
        confirm_btn.setFixedSize(200, 50)
        confirm_btn.setFont(QFont("Arial", 14, QFont.Bold))
        confirm_btn.setStyleSheet("background-color: blue; color: white; border-radius: 8px;")
        confirm_btn.clicked.connect(self.click_confirm_btn)

        self.table_list = QTableWidget()
        self.table_list.setColumnCount(2)
        self.table_list.setHorizontalHeaderLabels(["차량번호", "입차시간"])
        self.table_list.setFont(QFont("Arial", 10))
        self.table_list.setSelectionMode(QTableWidget.SingleSelection)
        self.table_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_list.itemSelectionChanged.connect(self.car_select)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.car_img_widget)
        left_layout.addSpacing(10)
        left_layout.addWidget(confirm_btn)

        content_layout = QHBoxLayout()
        content_layout.addLayout(left_layout)
        content_layout.addWidget(self.table_list)

        main_layout = QVBoxLayout()
        main_layout.addWidget(guide_label)
        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

    def load_data(self, car_list):
        self.car_list = car_list
        self.table_list.setRowCount(len(car_list))
        for i, car in enumerate(car_list):
            self.table_list.setItem(i, 0, QTableWidgetItem(car["번호"]))
            self.table_list.setItem(i, 1, QTableWidgetItem(car["입차시간"]))
        if car_list:
            self.table_list.selectRow(0)

    def car_select(self):
        selected = self.table_list.selectionModel().selectedRows()
        if selected:
            row = selected[0].row()
            self.car_number = self.table_list.item(row, 0).text()
            self.entry_time = self.table_list.item(row, 1).text()

            img_path = f"{base_path}/img/car_{self.car_number}.png"
            if os.path.exists(img_path):
                self.car_img_widget.setStyleSheet(f"border-image: url({img_path}); background-position: center; background-repeat: no-repeat;")
            else:
                self.car_img_widget.setText("이미지 없음")
        else:
            self.car_img_widget.setText("차량을 선택하세요")

    def click_confirm_btn(self):
        if hasattr(self, 'car_number') and hasattr(self, 'entry_time'):
            self.on_confirm_callback(self.car_number, self.entry_time)
        else:
            print("선택된 차량이 없습니다.")

if __name__ == "__main__":
    def handle_car_selection(car_number, entry_time):
        print("[콜백 호출됨]")
        print("차량번호:", car_number)
        print("입차시간:", entry_time)

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
