import tkinter as tk

class Recipe:
    def __init__(self, root):
        self.root = root
        self.count = 0
        self.stop_event = False

        # Label to display self.count
        self.count_label = tk.Label(root, text="Count: 0", font=('Arial', 12))
        self.count_label.grid(row=2, column=0, columnspan=5)

        # Start button
        self.start_button = tk.Button(root, text="Start", command=self.startRecipe)
        self.start_button.grid(row=3, column=0, columnspan=5)

    def stopRecipe(self):
        self.stop_event = True

    def startRecipe(self):
        self.stop_event = False
        self.goRecipe()

    def goRecipe(self):
        if not self.stop_event and self.count < 20:
            self.count += 1
            self.updateCountLabel()  # self.count가 변경될 때마다 라벨 업데이트
            self.root.after(1000, self.goRecipe)  # 1초 후에 goRecipe() 호출

    def updateCountLabel(self):
        self.count_label.config(text=f"Count: {self.count}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Recipe(root)
    root.mainloop()
