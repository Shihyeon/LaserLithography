import time

class Recipe:
    def __init__(self, window):
        self.window = window
        self.count = 0
        self.stop_event = False

    def stopRecipe(self):
        self.stop_event = True

    def startRecipe(self):
        self.stop_event = False
        self.goRecipe()

    def goRecipe(self):
        if not self.stop_event and self.count < 20:
            self.count += 1
            self.updateCountLabel()
            self.window.root.after(1000, self.goRecipe)

    def updateCountLabel(self):
        self.window.count_label.config(text=f"Count: {self.count}")
