import tkinter as tk
from controller.testrecipe import Recipe

class Window:
    def __init__(self, root):
        self.root = root
        self.recipe = Recipe(self)

        self.count_label = tk.Label(root, text="Count: 0", font=('Arial', 12), relief="groove")
        self.count_label.grid(row=2, column=0, columnspan=5)

        self.start_button = tk.Button(root, text="Start", command=self.recipe.startRecipe)
        self.start_button.grid(row=3, column=0, columnspan=2)
        
        self.stop_button = tk.Button(root, text="Stop", command=self.recipe.stopRecipe)
        self.stop_button.grid(row=3, column=3, columnspan=2)

    def updateCountLabel(self):
        self.count_label.config(text=f"Count: {self.recipe.count}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Window(root)
    root.mainloop()
