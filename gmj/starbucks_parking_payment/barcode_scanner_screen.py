import sys
import cv2
import os
from PyQt5.QtWidgets import (
    QApplication, QLabel, QWidget, QPushButton, QVBoxLayout, QSizePolicy
)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from datetime import datetime
from barcode_scanner import BarcodeScannerWorker
from sbuck_style import SBUCKStyle

class BarcodeScannerApp(QWidget):
    def __init__(self, on_barcode_callback):
        super().__init__()
        self.on_barcode_callback = on_barcode_callback
        self.initUI()
        self.setFixedSize(SBUCKStyle.WINDOW_WIDTH, SBUCKStyle.WINDOW_HEIGHT)

    def initUI(self):
        self.setWindowTitle('바코드 스캐너')
        self.resize(SBUCKStyle.WINDOW_WIDTH, SBUCKStyle.WINDOW_HEIGHT)
        self.setStyleSheet(f"background-color: {SBUCKStyle.COLOR_BG};")

        # ───── 카메라 화면 ─────
        self.video_label = QLabel("카메라 화면")
        self.video_label.setFixedSize(320, 200)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet(SBUCKStyle.STYLE_VIDEO_FRAME)

        # ───── 바코드 정보 출력 ─────
        self.barcode_info = QLabel("")
        self.barcode_info.setFixedHeight(60)
        self.barcode_info.setFixedWidth(320)
        self.barcode_info.setAlignment(Qt.AlignCenter)
        self.barcode_info.setStyleSheet(SBUCKStyle.STYLE_BARCODE_INFO)

        # ───── 스캔 버튼 ─────
        self.scan_button = QPushButton("스캔 시작")
        self.scan_button.setFixedHeight(50)
        self.scan_button.setFixedWidth(320)
        self.scan_button.setFont(SBUCKStyle.FONT_BUTTON)
        self.scan_button.setStyleSheet(SBUCKStyle.STYLE_CONFIRM_BTN)
        self.scan_button.clicked.connect(self.start_scanning)

        # ───── 내부 컨테이너로 중앙 정렬 ─────
        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setSpacing(15)
        container_layout.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(self.video_label)
        container_layout.addWidget(self.barcode_info)
        container_layout.addWidget(self.scan_button)
        container.setLayout(container_layout)

        main_layout = QVBoxLayout()
        main_layout.addStretch(1)
        main_layout.addWidget(container, alignment=Qt.AlignCenter)
        main_layout.addStretch(1)
        main_layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(main_layout)

    def start_scanning(self):
        self.scan_button.setEnabled(False)  # ✅ 중복 클릭 방지
        self.barcode_info.setText("스캔 중입니다...")  # ✅ 상태 표시
        self.scanner_worker = BarcodeScannerWorker()
        self.scanner_worker.frameCaptured.connect(self.update_frame)
        self.scanner_worker.barcodeDetected.connect(self.display_barcode_info)
        self.scanner_worker.start()

    def update_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qt_image))

    def display_barcode_info(self, barcode_data):
        obj_nowdate = datetime.strptime(barcode_data.split('-')[0], "%Y%m%d%H%M%S")
        free_amount = barcode_data.split('-')[1]

        self.barcode_info.setText(
            f"날짜: {obj_nowdate.date()}\n시간: {obj_nowdate.time()}\n가격: {free_amount}"
        )
        print(f"[스캔 결과] {barcode_data}")
        self.on_barcode_callback(barcode_data)
        self.close_app()

    def close_app(self):
        self.scanner_worker.stop()

if __name__ == '__main__':
    def dummy_callback(data):
        print("Scanned barcode:", data)

    app = QApplication(sys.argv)
    window = BarcodeScannerApp(dummy_callback)
    window.show()
    sys.exit(app.exec_())
