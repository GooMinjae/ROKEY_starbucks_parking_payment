import sys
import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QTextEdit, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from datetime import datetime
from barcode_thread import BarcodeScannerWorker

class BarcodeScannerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('바코드 스캐너')
        self.setGeometry(100, 100, 640, 480)
        
        self.video_label = QLabel(self, text="카메라 화면")
        self.video_label.setFixedSize(640, 480)
        self.video_label.setAlignment(Qt.AlignCenter)

        self.scan_button = QPushButton("스캔 시작")
        self.scan_button.clicked.connect(self.start_scanning)
        
        # self.barcode_info = QTextEdit(self)
        # self.barcode_info.setReadOnly(True)
        self.barcode_info = QLabel("")
        self.barcode_info.setAlignment(Qt.AlignCenter)
        self.barcode_info.setFixedHeight(80)
        
        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.barcode_info)
        layout.addWidget(self.scan_button)
        self.setLayout(layout)
    
    def start_scanning(self):
        self.scanner_worker = BarcodeScannerWorker()
        self.scanner_worker.frameCaptured.connect(self.update_frame)
        self.scanner_worker.barcodeDetected.connect(self.display_barcode_info)
        self.scanner_worker.start()  # 앱 실행 시 자동으로 스캐너 시작


    def update_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qt_image))
    
    def display_barcode_info(self, barcode_data):
        obj_nowdate = datetime.strptime(barcode_data.split('-')[0], "%Y%m%d%H%M%S")
        free_amount = barcode_data.split('-')[1]

        self.barcode_info.setText(f'날짜: {obj_nowdate.date()}\n시간: {obj_nowdate.time()}\n가격: {free_amount}')
        # print(f'날짜: {info["date"]}\n시간: {info["time"]}\n가격: {info["price"]}')   # 테스트용 출력
        self.close_app()
    
    def close_app(self):
        self.scanner_worker.stop()
        # self.close()

    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key_Q:  # 'q' 버튼 누르면 종료
    #         self.close_app()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BarcodeScannerApp()
    window.show()
    # sys.exit(app.exec_())
    app.exec_()
    window.scanner_worker.stop()