from sys import argv
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QFont ,QPixmap
from PyQt5.QtCore import Qt, QTimer
from exit_screen import ExitScreen


class ParkingInfoTable(QWidget):
    def __init__(self, callback, car_info, park_info):
        super().__init__()
        self.callback = callback
        [self.car_num, self.car_path] = car_info
        [self.entry_time, self.parking_time, self.parking_fee, self.free_fee, self.pay_amount] = park_info

        self.setWindowTitle("I PARKING 주차정산기 - 차량 요금 정산")
        main_layout = QHBoxLayout()
        car_layout = QVBoxLayout()
        info_layout = QGridLayout()
        info_layout.setSpacing(0)

        # Car Image
        self.img_lbl = QLabel()
        self.img_lbl.setPixmap(QPixmap())
        self.img_lbl.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(self.car_path).scaled(300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.img_lbl.setPixmap(pixmap)
        car_layout.addWidget(self.img_lbl)

        # Car Number
        self.plate_lbl = QLabel(self.car_num)
        self.plate_lbl.setFont(QFont("Arial", 20))
        self.plate_lbl.setAlignment(Qt.AlignCenter)
        car_layout.addWidget(self.plate_lbl)
        main_layout.addLayout(car_layout)

        # Payment Infomation
        labels = [
            ("입차 시각", self.entry_time),
            ("주차 시간", self.parking_time),
            ("주차 요금", self.parking_fee),
            ("할인 금액", self.free_fee),
            ("결제 금액", self.pay_amount),
        ]

        for i, (key, value) in enumerate(labels):
            key_label = QLabel(key)
            value_label = QLabel(value)

            key_label.setFont(QFont("Arial", 10))
            key_label.setAlignment(Qt.AlignCenter)
            key_label.setFixedWidth(120)
            value_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            if key == "할인 금액":
                key_label.setStyleSheet("border: 1px solid gray; padding: 6px; background-color: #2979ff; color: white;")
                value_label.setFont(QFont("Arial", 11, QFont.Bold))
                value_label.setStyleSheet("border: 1px solid gray; padding: 6px; color: #2979ff;")
            elif key == "결제 금액":
                key_label.setStyleSheet("border: 1px solid gray; padding: 6px; background-color: #d32f2f; color: white;")
                value_label.setFont(QFont("Arial", 14, QFont.Bold))
                value_label.setStyleSheet( "border: 1px solid gray; padding: 6px; color: #d32f2f;")
            else:
                key_label.setStyleSheet("border: 1px solid gray; padding: 6px; background-color: #f0f0f0;")
                value_label.setFont(QFont("Arial", 11, QFont.Bold))
                value_label.setStyleSheet("border: 1px solid gray; padding: 6px;")

            info_layout.addWidget(key_label, i, 0)
            info_layout.addWidget(value_label, i, 1)

        main_layout.addLayout(info_layout)
        self.setLayout(main_layout)

        QTimer.singleShot(2000, self.callback)


if __name__ == '__main__':
    from os import path

    class AppController:
        def __init__(self):
            base_path = path.dirname(path.realpath(__file__))
            base_path = base_path.replace("\\", "/")
            carNum = '112가 4567'

            carInfo = [carNum, f"{base_path}/img/car_{carNum}.png"]
            parkInfo = ["2014.11.18 08:19:22",
                        "2시간 38분",
                        "14,500 원",
                        "3,500 원",
                        "11,000 원"]
            
            self.app = QApplication(argv)
            self.parking_screen = ParkingInfoTable(self.show_exit_screen, carInfo, parkInfo)
            self.exitScreen = ExitScreen()

        def show_exit_screen(self):
            self.parking_screen.close()
            self.exitScreen.show()
            self.exitScreen.play_voice()

        def run(self):
            self.parking_screen.show()
            exit(self.app.exec_())
    
    controller = AppController()
    controller.run()