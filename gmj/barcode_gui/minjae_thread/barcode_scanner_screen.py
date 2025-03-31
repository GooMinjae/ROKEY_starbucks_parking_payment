# main_gui.py
import sys
import threading
import time
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from barcode_scanner import BarcodeScanner

class BarcodeSignal(QObject):
    frame_updated = pyqtSignal(QImage)
    barcode_detected = pyqtSignal(dict)

class BarcodeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Threaded Barcode Scanner")

        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.result_label = QLabel("바코드 정보를 기다리는 중...")

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.result_label)
        self.setLayout(layout)

        self.signals = BarcodeSignal()
        self.signals.frame_updated.connect(self.update_image)
        self.signals.barcode_detected.connect(self.show_result)

        self.scanner = BarcodeScanner()
        self.thread = threading.Thread(target=self.camera_loop)
        self.stop_event = threading.Event()

        if self.scanner.start():
            self.thread.start()
        else:
            self.result_label.setText("카메라를 열 수 없습니다.")

    def camera_loop(self):
        while not self.stop_event.is_set():
            frame = self.scanner.read_frame()
            if frame is None:
                continue

            info = self.scanner.recognize(frame)
            if info:
                x, y, w, h = info['rect']
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, info['text'], (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                self.signals.barcode_detected.emit(info)
                self.stop_event.set()

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb.shape
            qimg = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
            self.signals.frame_updated.emit(qimg)

            time.sleep(0.03)  # ~30fps

    def update_image(self, qimg):
        self.video_label.setPixmap(QPixmap.fromImage(qimg))

    def show_result(self, info):
        self.result_label.setText(
            f"바코드 인식 완료:\n날짜: {info['date']}\n시간: {info['time']}\n금액: {info['price']}원"
        )

    def closeEvent(self, event):
        self.stop_event.set()
        if self.thread.is_alive():
            self.thread.join()
        self.scanner.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BarcodeApp()
    window.show()
    sys.exit(app.exec_())
