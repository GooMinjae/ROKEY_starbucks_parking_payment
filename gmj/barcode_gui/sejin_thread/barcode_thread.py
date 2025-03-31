import cv2
import threading
from pyzbar.pyzbar import decode
import winsound
from PyQt5.QtCore import pyqtSignal, QObject
from datetime import datetime

class BarcodeScannerWorker(QObject):
    frameCaptured = pyqtSignal(object)  # 프레임 업데이트 신호
    barcodeDetected = pyqtSignal(dict)  # 바코드 정보 신호

    def __init__(self):
        super().__init__()
        self.running = False
        self.cap = cv2.VideoCapture(0)
        self.thread = None  # 스레드 객체

    def start(self):
        if self.thread is None or not self.thread.is_alive():  # 기존 스레드가 없거나 종료되었을 때만 실행
            self.running = True
            self.thread = threading.Thread(target=self.run)
            self.thread.start()

    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue
            
            processed_frame, barcode_info, detected = self.recognize_barcode(frame)
            self.frameCaptured.emit(processed_frame)
            
            if detected:
                self.barcodeDetected.emit(barcode_info)
                self.running = False
                
        self.cap.release()
    
    def recognize_barcode(self, frame):
        barcodes = decode(frame)
        info = {}
        for barcode in barcodes:
            if barcode.type == 'PDF417':
                continue
            x, y, w, h = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            barcode_data = barcode.data.decode('utf-8')
            barcode_type = barcode.type
            text = f'{barcode_type}: {barcode_data}'
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.9, (0, 255, 0), 2)
            winsound.Beep(1000, 200)
            
            try:
                obj_nowdate = datetime.strptime(barcode_data[:14], "%Y%m%d%H%M%S")
                formatted_date = obj_nowdate.strftime("%Y-%m-%d")
                formatted_time = obj_nowdate.strftime("%H:%M:%S")
                info = {'date': formatted_date, 'time': formatted_time, 'price': barcode_data[14:]}
            except ValueError:
                info = {'date': 'Invalid', 'time': 'Invalid', 'price': barcode_data[14:]}
            
            return frame, info, True
        return frame, info, False
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    worker = BarcodeScannerWorker()

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame, info, detected = worker.recognize_barcode(frame)
        cv2.imshow("Barcode Scanner", frame)

        if detected:
            print("바코드 감지됨:")
            print(f"날짜: {info['date']}, 시간: {info['time']}, 가격: {info['price']}")
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()