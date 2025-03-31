# barcode_scanner.py
import cv2
from pyzbar.pyzbar import decode

class BarcodeScanner:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None
        self.running = False

    def start(self):
        self.cap = cv2.VideoCapture(self.camera_index)
        self.running = self.cap.isOpened()
        return self.running

    def stop(self):
        self.running = False
        if self.cap and self.cap.isOpened():
            self.cap.release()

    def read_frame(self):
        if not self.running:
            return None
        ret, frame = self.cap.read()
        return frame if ret else None

    def recognize(self, frame):
        barcodes = decode(frame)
        for barcode in barcodes:
            if barcode.type == 'PDF417':
                continue
            x, y, w, h = barcode.rect
            barcode_data = barcode.data.decode('utf-8')
            return {
                'date': barcode_data[:8],
                'time': barcode_data[8:14],
                'price': barcode_data[14:],
                'rect': (x, y, w, h),
                'text': f'{barcode.type}: {barcode_data}'
            }
        return None
