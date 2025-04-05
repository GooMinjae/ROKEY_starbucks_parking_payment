import cv2
from pyzbar.pyzbar import decode

# 0: 기본 웹캠
# 외부 카메라 사용 시 번호 변경
cap = cv2.VideoCapture(0)

print("바코드를 스캔하려면 웹캠 앞에 바코드를 보여주세요. 'q'를 누르면 종료됩니다.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 바코드 인식
    barcodes = decode(frame)

    for barcode in barcodes:
        # 바코드 영역에 사각형 그리기
        x, y, w, h = barcode.rect
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # 바코드 데이터 디코딩
        barcode_data = barcode.data.decode('utf-8')
        barcode_type = barcode.type

        # 텍스트로 바코드 정보 표시
        text = f'{barcode_type}: {barcode_data}'
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, (0, 255, 0), 2)

        print(f'[INFO] 바코드 인식됨: {barcode_type} - {barcode_data}')

    # 화면에 표시
    cv2.imshow('Barcode Scanner', frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 리소스 해제
cap.release()
cv2.destroyAllWindows()