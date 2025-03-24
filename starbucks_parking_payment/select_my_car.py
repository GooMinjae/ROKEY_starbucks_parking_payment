# SelectMyCarInfoScreen
# 다른 시스템, 모듈 연동 고려
# 스스로 더미 데이터 만들어 코드 작성, Unit Test

from datetime import datetime, timedelta

    # 차량 데이터 샘플
entry_time = datetime.now()

car_data_list = [
    {"번호": "123가 4567", "입차시간": (entry_time - timedelta(minutes=20)).strftime("%Y-%m-%d %H:%M:%S")},
    {"번호": "245가 4567", "입차시간": (entry_time - timedelta(minutes=80)).strftime("%Y-%m-%d %H:%M:%S")},
    {"번호": "112가 4567", "입차시간": (entry_time - timedelta(minutes=120)).strftime("%Y-%m-%d %H:%M:%S")}
]


import sys 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os

base_path = os.path.dirname(os.path.realpath(__file__))
base_path = base_path.replace("\\", "/")

class SelectMyCarInfoScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iPARKING 주차정산기(GooMinjae)")
        self.setGeometry(300, 300, 600, 400)
        self.setStyleSheet("background-color: #252E3E;")

        # guide label
        guide_label = QLabel()
        # guide_label.setText('<span style="color: #FFFFFF; font-family: Arial, sans-serif; font-size: 25px;">\
        #                         차량번호 4자리 입력 후<br><span style="color: #496B91;">확인</span> 버튼을 눌러주세요\
        #                     </span>')
        guide_label.setText('고객님 차량을 선택하신 후 확인 버튼을 눌러주세요')
        guide_label.setAlignment(Qt.AlignCenter)
        guide_label.setFont(QFont("Arial", 12))
        guide_label.setStyleSheet("color: #FFFFFF;")
        # guide_label.setFixedSize(300, 60)


        tabel_list = QTableWidget()
        for i, value in enumerate(car_data_list):
            tabel_list.setItem(i, 0, QTableWidgetItem(value["번호"]))
            tabel_list.setItem(i, 1, QTableWidgetItem(value["입차시간"]))


        
        main_layout = QHBoxLayout()
        main_layout.addWidget(guide_label)
        main_layout.addWidget(tabel_list)
        self.setLayout(main_layout)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SelectMyCarInfoScreen()
    win.show()
    app.exec_()
