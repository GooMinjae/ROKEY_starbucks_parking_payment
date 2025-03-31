import cv2
from pyzbar.pyzbar import decode
import winsound
from datetime import datetime

class Barcode:
    def __init__(self):
        self.detected = False

    def recognize_barcode(self, frame):
        barcodes = decode(frame)
        info = {}
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
            info = {'date':barcode_data[:8], 'time':barcode_data[8:14], 'price':barcode_data[14:]}
            self.detected = True
            return frame, info, True  # 인식되면 True 반환 → 종료
        return frame, info, False  # 인식 안 됨


# 단위 테스트
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    print("바코드를 스캔하려면 웹캠 앞에 바코드를 보여주세요.")
    barcode = Barcode()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("웹캠을 사용할 수 없습니다.")
            break
        processed_frame, barcode_info, detected = barcode.recognize_barcode(frame)
        cv2.imshow("Barcode Scanner", processed_frame)
        if detected:    # 바코드 인식되면 종료
            nowdate = datetime.strptime(barcode_info, '%Y%m%d%H%M%S') ############### 이후에 수정 필요
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):   # 'q'로 수동 종료도 가능
            break

    cap.release()
    cv2.destroyAllWindows()


# PyQt 연동 시 사용 예시 코드
# ret, frame = self.cap.read()
# if ret:
#     processed_frame, barcode_info, detected = self.barcode.recognize_barcode(frame) # return frame, info, True
#     # processed_frame을 QLabel 등에 표시
#     if detected:
#         self.timer.stop()  # 또는 필요한 동작 수행