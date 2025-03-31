import threading
import time

# 스레드 클래스 정의
class MyWorkerThread(threading.Thread):
    def __init__(self, callback=None):
        super().__init__()
        self.callback = callback  # 작업 완료 후 호출할 함수
        self.running = True

    def run(self):
        print("[스레드] 작업 시작")
        for i in range(5):
            if not self.running:
                break
            print(f"[스레드] {i + 1}초 작업 중...")
            time.sleep(0.5)

        result = "작업 결과: 성공"
        print("[스레드] 작업 완료")

        if self.callback:
            self.callback(result)  # 결과 전달

    def stop(self):
        self.running = False



# 메인 실행
if __name__ == "__main__":
    print("[메인] 프로그램 시작")

    # 콜백 함수
    def handle_result(result):
        print(f"[콜백] 스레드에서 전달받은 결과: {result}")

    # 스레드 생성 및 시작
    worker = MyWorkerThread(callback=handle_result)
    worker.start()

    # 메인 루프
    for i in range(10):
        print(f"[메인] Main is running... {i + 1}")
        time.sleep(1)

    # 스레드 종료 대기
    worker.join()
    print("[메인] 모든 작업 종료")
