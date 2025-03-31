import sys
import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from barcode_thread import BarcodeScannerWorker

class BarcodeScannerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.scanner_worker = BarcodeScannerWorker()
        self.scanner_worker.frameCaptured.connect(self.update_frame)
        self.scanner_worker.barcodeDetected.connect(self.display_barcode_info)
        self.scanner_worker.start()  # 앱 실행 시 자동으로 스캐너 시작

    def initUI(self):
        self.setWindowTitle('바코드 스캐너')
        self.setGeometry(100, 100, 640, 480)
        
        self.video_label = QLabel(self)
        self.video_label.setFixedSize(640, 480)
        self.video_label.setAlignment(Qt.AlignCenter)
        
        self.barcode_info = QTextEdit(self)
        self.barcode_info.setReadOnly(True)
        
        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.barcode_info)
        self.setLayout(layout)
    
    def update_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qt_image))
    
    def display_barcode_info(self, info):
        self.barcode_info.append(f'날짜: {info["date"]}\n시간: {info["time"]}\n가격: {info["price"]}')
        print(f'날짜: {info["date"]}\n시간: {info["time"]}\n가격: {info["price"]}')   # 테스트용 출력
        self.close_app()
    
    def close_app(self):
        self.scanner_worker.stop()
        self.close()

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