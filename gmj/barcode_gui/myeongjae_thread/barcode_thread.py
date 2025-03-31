import sys
import cv2
import threading
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QEvent
from barcode_scanner import Barcode  # 기존 Barcode 클래스 사용
class BarcodeScannerScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("바코드 스캐너")
        self.setGeometry(200, 200, 640, 480)
        self.label = QLabel("카메라 화면")
        self.label.setAlignment(Qt.AlignCenter)
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.button = QPushButton("스캔 시작")
        self.button.clicked.connect(self.start_scanning)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.result_label)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.running = False
        self.thread = None
        self.cap = None
        self.barcode = Barcode()
    def start_scanning(self):
        if not self.running:
            self.running = True
            self.result_label.setText("스캔 중...")
            self.cap = cv2.VideoCapture(0)
            self.thread = threading.Thread(target=self.scan_loop)
            self.thread.start()
    def scan_loop(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue
            processed_frame, info, detected = self.barcode.recognize_barcode(frame)
            rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb.shape
            bytes_per_line = ch * w
            qimg = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg)
            self.update_ui_safe(pixmap, info if detected else None)
            if detected:
                break
        self.running = False
        if self.cap:
            self.cap.release()
    def update_ui_safe(self, pixmap, info):
        event = _FunctionEvent(lambda: self.update_ui(pixmap, info))
        QApplication.postEvent(self, event)
    def update_ui(self, pixmap, info):
        self.label.setPixmap(pixmap)
        if info:
            self.result_label.setText(
                f"날짜: {info['date']}\n시간: {info['time']}\n금액: {info['price']}"
            )
    def customEvent(self, event):
        if isinstance(event, _FunctionEvent):
            event.callback()
    def closeEvent(self, event):
        self.running = False
        if self.cap:
            self.cap.release()
        event.accept()
class _FunctionEvent(QEvent):
    EVENT_TYPE = QEvent.Type(QEvent.registerEventType())
    def __init__(self, callback):
        super().__init__(self.EVENT_TYPE)
        self.callback = callback
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = BarcodeScannerScreen()
    win.show()
    # sys.exit(app.exec_())
    app.exec_()
    win.running = False