import sys
import pyttsx3
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from os import _exit

class ExitScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("I PARKING 주차정산기 - 정산 완료")
        self.setFixedSize(400, 400)
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Text Label
        self.text_label = QLabel("이용해 주셔서\n감사합니다")
        self.text_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.text_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.text_label)

        self.setLayout(layout)

    def play_voice(self):
        engine = pyttsx3.init()
        engine.setProperty('voice',r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_KO-KR_HEAMI_11.0')
        engine.setProperty('rate', 140)
        engine.say("이용해 주셔서 감사합니다.")
        engine.runAndWait()
        self.close()
    
    def closeEvent(self, event):
        _exit(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ExitScreen()
    window.show()
    window.play_voice()
    sys.exit(app.exec_())