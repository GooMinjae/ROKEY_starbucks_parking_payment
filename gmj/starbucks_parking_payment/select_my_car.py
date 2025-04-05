import sys 
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QTableWidget,
    QHeaderView, QTableWidgetItem, QAbstractItemView,
    QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import Qt
from sbuck_style import SBUCKStyle
from datetime import datetime, timedelta
import os

class SelectMyCarInfoScreen(QWidget):
    def __init__(self, on_confirm_callback):
        super().__init__()
        self.setWindowTitle("iPARKING - 차량번호 확인")
        self.setStyleSheet(f"background-color: {SBUCKStyle.COLOR_BG};")
        self.car_list = []
        self.on_confirm_callback = on_confirm_callback
        self.setFixedSize(SBUCKStyle.WINDOW_WIDTH, SBUCKStyle.WINDOW_HEIGHT)

        # ───── 안내 라벨 ─────
        guide_label = QLabel("고객님 차량을 선택하신 후 <span style='color: #134F9E;'>확인</span> 버튼을 눌러주세요")
        guide_label.setAlignment(Qt.AlignCenter)
        guide_label.setStyleSheet(SBUCKStyle.STYLE_LABEL_BOLD)
        guide_label.setFixedHeight(70)

        # ───── 차량 이미지 위젯 ─────
        self.car_img_widget = QWidget()
        self.car_img_widget.setFixedSize(250, 250)
        default_img_path = f"{SBUCKStyle.BASE_PATH}/img/cars/default_car.png"
        self.car_img_widget.setStyleSheet(SBUCKStyle.STYLE_CAR_IMAGE_BOX % default_img_path)

        # ───── 확인 버튼 ─────
        confirm_btn = QPushButton("확  인")
        confirm_btn.setStyleSheet(SBUCKStyle.STYLE_CONFIRM_BTN)
        confirm_btn.setFont(SBUCKStyle.FONT_BUTTON)
        confirm_btn.setFixedSize(250, 50)
        confirm_btn.clicked.connect(self.click_confirm_btn)

        # ───── 차량 목록 테이블 ─────
        self.table_list = QTableWidget()
        self.table_list.setColumnCount(2)
        self.table_list.setHorizontalHeaderLabels(["차량번호", "입차시간"])
        self.table_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_list.setSelectionMode(QTableWidget.SingleSelection)
        self.table_list.setSelectionBehavior(QTableWidget.SelectRows)
        self.table_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_list.itemSelectionChanged.connect(self.car_select)
        self.table_list.setMinimumHeight(250)
        self.table_list.setMaximumWidth(400)
        self.table_list.setStyleSheet(SBUCKStyle.STYLE_TABLE)

        # ───── 레이아웃 ─────
        car_img_layout = QVBoxLayout()
        car_img_layout.addWidget(self.car_img_widget)
        car_img_layout.addSpacing(10)
        car_img_layout.addWidget(confirm_btn)
        car_img_layout.setAlignment(Qt.AlignTop)

        car_info_layout = QHBoxLayout()
        car_info_layout.setContentsMargins(20, 10, 20, 10)
        car_info_layout.setSpacing(30)
        car_info_layout.addLayout(car_img_layout)
        car_info_layout.addWidget(self.table_list)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.addWidget(guide_label)
        main_layout.addLayout(car_info_layout)
        self.setLayout(main_layout)

    def load_data(self, car_list):
        self.car_list = car_list
        self.table_list.setRowCount(len(self.car_list))

        for i, value in enumerate(self.car_list):
            self.table_list.setItem(i, 0, QTableWidgetItem(value["번호"]))
            self.table_list.setItem(i, 1, QTableWidgetItem(value["입차시간"]))
        self.table_list.selectRow(0)

    def car_select(self):
        self.selected_rows = self.table_list.selectionModel().selectedRows()
        if self.selected_rows:
            row = self.selected_rows[0].row()
            self.car_number = self.table_list.item(row, 0).text()
            self.entry_time = self.table_list.item(row, 1).text()

            car_img = f"{SBUCKStyle.BASE_PATH}/img/cars/car_{self.car_number}.png"
            self.car_img_widget.setStyleSheet(SBUCKStyle.STYLE_CAR_IMAGE_BOX % car_img)

    def click_confirm_btn(self):
        if self.selected_rows:
            self.on_confirm_callback(self.car_number, self.entry_time)

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
