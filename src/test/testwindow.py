import tkinter as tk
from testrecipe import Recipe

class Window:
    def __init__(self, root):
        self.root = root
        self.recipe = Recipe(self)  # Recipe 인스턴스 생성 및 Window 인스턴스 전달

        self.count_label = tk.Label(root, text="Count: 0", font=('Arial', 12))
        self.count_label.grid(row=2, column=0, columnspan=5)

        self.start_button = tk.Button(root, text="Start", command=self.recipe.startRecipe)
        self.start_button.grid(row=3, column=0, columnspan=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = Window(root)
    root.mainloop()
