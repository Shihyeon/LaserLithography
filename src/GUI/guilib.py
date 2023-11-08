import tkinter as tk

class Guilib():
    def setFrame(self, root, row, column, rowspan=1, columnspan=1):
        self.frame = tk.Frame(root)
        self.frame.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan)
        return self.frame
        
    def setTitle(self, frame, row, column, text, rowspan=1, columnspan=1, width=30, font=('Arial', 20)):
        self.title_label = tk.Label(frame, text=text, width=width, font=font)
        self.title_label.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan)
        
    def setSubTitle(self, frame, row, column, text, rowspan=1, columnspan=1, font=('Arial', 12)):
        self.subtitle_label = tk.Label(frame, text=text, font=font)
        self.subtitle_label.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan)
        
    def setEmptyBox(self, frame, row, column, width=1, height=1):
        self.emptybox = tk.Label(frame, width=width, height=height)
        self.emptybox.grid(row=row, column=column)
        
    def setAxisInputLabel(self, frame, row, column, text, font=('Arial', 11)):
        self.x_label = tk.Label(frame, text=text, width=2, font=font)
        self.x_label.grid(row=row, column=column)
        self.x_entry = tk.Entry(self.frame2, width=10, font=('Arial', 11))
        self.x_entry.grid(row=row, column=column+1)