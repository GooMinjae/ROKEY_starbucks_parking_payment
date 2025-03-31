import sys
import cv2
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import QTimer
from PySide6.QtGui import QImage, QPixmap
from barcode_scanner import Barcode

class BarcodeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Barcode Scanner GUI")
        self.video_label = QLabel()
        self.result_label = QLabel("결과 출력 대기 중...")

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.result_label)
        self.setLayout(layout)

        self.cap = cv2.VideoCapture(0)
        self.scanner = Barcode()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # 30ms 간격 (약 30fps)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return
        frame, info, detected = self.scanner.recognize_barcode(frame)
        if detected:
            self.result_label.setText(
                f"날짜: {info['date']} / 시간: {info['time']} / 금액: {info['price']}원"
            )
            self.timer.stop()  # 인식되면 중지
        # Draw rectangle and text
        if info.get("rect"):
            x, y, w, h = info["rect"]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, info["text"], (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        qimg = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qimg))

    def closeEvent(self, event):
        self.timer.stop()
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BarcodeApp()
    window.show()
    sys.exit(app.exec())
