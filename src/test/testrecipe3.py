import threading
import time

class Recipe:
    def __init__(self, app):
        self.count = 0
        self.stop_event = threading.Event()
        self.app = app

    def stopRecipe(self):
        self.stop_event.set()

    def startRecipe(self):
        self.stop_event.clear()
        threading.Thread(target=self.goRecipe).start()  # 새 스레드에서 goRecipe 실행

    def goRecipe(self):
        csv_size = 20
        for self.count in range(csv_size):
            if self.stop_event.is_set():
                break
            self.updateCountLabel()
            time.sleep(1)

    def updateCountLabel(self):
        self.app.root.after(0, self.app.updateCountLabel)  # GUI 업데이트 요청
