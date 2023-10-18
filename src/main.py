from Controller.motor import Motor
from GUI.gui import Window
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = Window.MotorControlWindow(root)
    root.mainloop()
