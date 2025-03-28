import cv2
from pyzbar.pyzbar import decode
import winsound
class Barcode:
    def __init__(self, cap):
        self.cap = cap
    def recognize_barcode(self):
        ret, frame = self.cap.read()
        if not ret:
            return False
        barcodes = decode(frame)
        for barcode in barcodes:
            if barcode.type == 'PDF417':  # PDF417 바코드는 무시
                continue
            x, y, w, h = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            barcode_data = barcode.data.decode('utf-8')
            barcode_type = barcode.type
            text = f'{barcode_type}: {barcode_data}'
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.9, (0, 255, 0), 2)
            winsound.Beep(1000, 200)
            print(f'[INFO] 바코드 인식됨: {barcode_type} - {barcode_data}')
            cv2.imshow('Barcode Scanner', frame)
            return True  # 인식되면 True 반환 → 종료
        cv2.imshow('Barcode Scanner', frame)
        return False  # 인식 안 됨
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    print("바코드를 스캔하려면 웹캠 앞에 바코드를 보여주세요.")
    barcode = Barcode(cap)
    while True:
        if barcode.recognize_barcode():  # 바코드 인식되면 종료
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q'로 수동 종료도 가능
            break
    cap.release()
    cv2.destroyAllWindows()