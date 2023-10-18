import tkinter as tk

class Window:
    def __init__(self, root):
        self.root = root
        self.root.title("Laser Lithography")
        
        # Frame1: Title Frame
        self.frame1 = self.addFrame(root, 0, 0)
        
        self.title1 = self.addTitle(self.frame1, 0, 0, text="Laser Lithography Control Window")
        
        self.empty1_10 = tk.Label(self.frame1, height=2)
        self.empty1_10.grid(row=1)
        
        # Frame2: Moving Commands Frame
        self.frame2 = self.addFrame(root, 1, 0)
        
        self.subtitle2_00 = self.addSubTitle(self.frame2, 0, 0, text="Move to Position.", columnspan=3)
        
        # X coordinate input field and label
        self.x_label = tk.Label(self.frame2, text="X:", width=2, font=('Nanumgothic', 11))
        self.x_label.grid(row=1, column=0)
        self.x_entry = tk.Entry(self.frame2, width=10, font=('Nanumgothic', 11))
        self.x_entry.grid(row=1, column=1)
        
        self.empty2_02 = tk.Label(self.frame2, width=2)
        self.empty2_02.grid(row=1, column=2)
        
        # Y coordinate input field and label
        self.y_label = tk.Label(self.frame2, text="Y:", width=2, font=('Nanumgothic', 11))
        self.y_label.grid(row=1, column=3)
        self.y_entry = tk.Entry(self.frame2, width=10, font=('Nanumgothic', 11))
        self.y_entry.grid(row=1, column=4)
        
        self.empty2_10 = tk.Label(self.frame2, height=1)
        self.empty2_10.grid(row=2, column=0)
        
        # Go button
        self.go_abs_button = tk.Button(self.frame2, text="Go Absolute", width=12, font=('Nanumgothic', 11))
        self.go_abs_button.grid(row=3, column=0, columnspan=2)
        
        # Stop button
        self.stop_button = tk.Button(self.frame2, text="Stop", width=12, font=('Nanumgothic', 11))
        self.stop_button.grid(row=3, column=3, columnspan=2)
        
        
        
        # Frame3: Exit Frame
        self.frame3 = self.addFrame(root, 3, 0)
        
        self.empty3_00 = tk.Label(self.frame3, height=2)
        self.empty3_00.grid(row=0)
        
        # Exit button
        self.exit_button = tk.Button(self.frame3, text="Exit", width=12, font=('Nanumgothic', 11))
        self.exit_button.grid(row=1)
        
        self.empty3_20 = tk.Label(self.frame3, height=2)
        self.empty3_20.grid(row=2)
        
        
    def addFrame(self, root, row, column, rowspan=1, columnspan=1):
        self.frame = tk.Frame(root)
        self.frame.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan)
        return self.frame
        
    def addTitle(self, frame, row, column, text, rowspan=1, columnspan=1, width=30, font=('Nanumgothic', 20)):
        self.title_label = tk.Label(frame, text=text, width=width, font=font)
        self.title_label.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan)
        
    def addSubTitle(self, frame, row, column, text, rowspan=1, columnspan=1, font=('Nanumgothic', 12)):
        self.subtitle_label = tk.Label(frame, text=text, font=font)
        self.subtitle_label.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan)
        
        

if __name__ == "__main__":
    root = tk.Tk()
    app = Window(root)
    root.mainloop()
