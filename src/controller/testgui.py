import tkinter as tk
import threading
import time
from testrecipe import Recipe
# from controller.motor import Motor

class Window:
    def __init__(self, root):
        self.root = root
        self.recipe = Recipe(self)
        self.app = self

        self.LargeFrame = tk.Frame(root)
        self.LargeFrame.pack(anchor="center")
        self.root.title("Laser Lithography")
        
        # Frame1: Title Frame
        self.title_frame = self.setFrame(self.LargeFrame, 0, 0)
        
        self.title1 = self.setTitle(self.title_frame, 0, 0, text="Laser Lithography Control Window")
        
        self.title_empty_10 = self.setEmptyBox(self.title_frame, 1, 0, height=2)
        
        # Frame2: Moving Commands Frame
        self.moving_frame = self.setFrame(self.LargeFrame, 1, 0)
        
        self.moving_subtitle_00 = self.setSubTitle(self.moving_frame, 0, 0, text="Test moving: Move to Position.", columnspan=5)
        
        self.x_label = self.setAxisInputLabel(self.moving_frame, 1, 0, text="X:")
        
        self.moving_empty_02 = tk.Label(self.moving_frame, width=2)
        self.moving_empty_02.grid(row=1, column=2)
        
        self.y_label = self.setAxisInputLabel(self.moving_frame, 1, 3, text="Y:")
        
        self.moving_empty_10 = tk.Label(self.moving_frame, height=1)
        self.moving_empty_10.grid(row=2, column=0)
        
        self.go_abs_button = tk.Button(self.moving_frame, text="Go Absolute", width=12, font=('Arial', 11), command=self.goAbsButton)
        self.go_abs_button.grid(row=3, column=0, columnspan=2)
        
        self.stop_button = tk.Button(self.moving_frame, text="Stop", width=12, font=('Arial', 11), command=self.stopAbsButton)
        self.stop_button.grid(row=3, column=3, columnspan=2)

        self.moving_empty_40 = self.setEmptyBox(self.moving_frame, 4, 0, height=2)
        
        # Frame3: Recipe operating Frame
        self.recipe_frame = self.setFrame(self.LargeFrame, 3, 0)

        self.recipe_subtitle_00 = self.setSubTitle(self.recipe_frame, 0, 0, text="Recipe operating.", columnspan=5)

        self.recipe_count_label = tk.Label(self.recipe_frame, text="- / -", font=('Arial', 12))
        self.recipe_count_label.grid(row=1, column=0, columnspan=5)

        self.run_recipe_button = tk.Button(self.recipe_frame, text="Run Recipe", width=12, font=('Arial', 11), command=self.startRecipeButton)
        self.run_recipe_button.grid(row=2, column=0, columnspan=2)

        self.recipe_empty_12 = tk.Label(self.recipe_frame, width=2)
        self.recipe_empty_12.grid(row=2, column=2)

        self.stop_recipe_button = tk.Button(self.recipe_frame, text="Stop Recipe", width=12, font=('Arial', 11), command=self.stopRecipeButton)
        self.stop_recipe_button.grid(row=2, column=3, columnspan=2)
        
        # Frame4: Exit Frame
        self.exit_frame = self.setFrame(self.LargeFrame, 4, 0)
        
        self.exit_empty_00 = tk.Label(self.exit_frame, height=2)
        self.exit_empty_00.grid(row=0)
        
        self.exit_button = tk.Button(self.exit_frame, text="Exit", width=12, font=('Arial', 11), command=self.closeWindowButton)
        self.exit_button.grid(row=1)
        
        self.exit_empty_20 = tk.Label(self.exit_frame, height=2)
        self.exit_empty_20.grid(row=2)
        
        
    def setFrame(self, root, row, column, rowspan=1, columnspan=1):
        self.frame = tk.Frame(root)
        self.frame.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan)
        return self.frame
        
    def setTitle(self, frame, row, column, text, rowspan=1, columnspan=1, width=30, font=('Arial', 20)):
        self.title_label = tk.Label(frame, text=text, width=width, font=font)
        self.title_label.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan)
        
    def setSubTitle(self, frame, row, column, text, rowspan=1, columnspan=1, bg="#E0E0E0", font=('Arial', 12)):
        self.subtitle_label = tk.Label(frame, text=text, bg=bg, font=font, justify=tk.LEFT, relief="groove")
        self.subtitle_label.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky='w')
        
    def setEmptyBox(self, frame, row, column, width=1, height=1):
        self.emptybox = tk.Label(frame, width=width, height=height)
        self.emptybox.grid(row=row, column=column)
        
    def setAxisInputLabel(self, frame, row, column, text, font=('Arial', 11)):
        self.x_label = tk.Label(frame, text=text, width=2, font=font)
        self.x_label.grid(row=row, column=column)
        self.x_entry = tk.Entry(self.moving_frame, width=10, font=('Arial', 11))
        self.x_entry.grid(row=row, column=column+1)
        
    def goAbsButton(self):
        # Disable command (버튼 커멘드가 실행되는 동안 다른 버튼을 비활성화 상태로 설정)
        self.go_abs_button.config(state=tk.DISABLED)
        self.run_recipe_button.config(state=tk.DISABLED)
        self.stop_recipe_button.config(state=tk.DISABLED)
        self.exit_button.config(state=tk.DISABLED)
        # code (아래에 실행할 코드 작성)
        pass
        print("On goAbsButto")
        # Enable command (실행이 끝나면 버튼을 다시 활성화 상태로 설정)
        self.go_abs_button.config(state=tk.NORMAL)
        self.run_recipe_button.config(state=tk.NORMAL)
        self.stop_recipe_button.config(state=tk.NORMAL)
        self.exit_button.config(state=tk.NORMAL)

    def stopAbsButton(self):
        if self.goAbsButton == True:
            self.go_abs_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)
            self.run_recipe_button.config(state=tk.DISABLED)
            self.stop_recipe_button.config(state=tk.DISABLED)
            self.exit_button.config(state=tk.DISABLED)

            pass
            print("On stopAbsButton")

            self.go_abs_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
            self.run_recipe_button.config(state=tk.NORMAL)
            self.stop_recipe_button.config(state=tk.NORMAL)
            self.exit_button.config(state=tk.NORMAL)

    # startRecipe
    def startRecipeButton(self):
        if not self.recipe.isRunning():  # 작업이 실행 중이지 않은 경우에만 실행
            self.go_abs_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)
            self.run_recipe_button.config(state=tk.DISABLED)
            self.exit_button.config(state=tk.DISABLED)

            start_thread = threading.Thread(target=self.runRecipeWithButtonControl)
            start_thread.start()

    def runRecipeWithButtonControl(self):
        self.recipe.startRecipe()
        print("On startRecipeButton")

        # Recipe 작업이 완료될 때까지 대기
        while self.recipe.isRunning():
            time.sleep(0.1)  # 일시적으로 대기, 이 과정을 수정하여 적절한 대기 방법으로 변경할 수 있습니다.

        # Recipe 작업이 끝나면 버튼 활성화
        self.app.root.after(0, self.runRecipeEnableButtons)

    def runRecipeEnableButtons(self):
        self.go_abs_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL)
        self.run_recipe_button.config(state=tk.NORMAL)
        self.exit_button.config(state=tk.NORMAL)

    # stopRecipe
    def stopRecipeButton(self):
        if self.recipe.isRunning():  # 작업이 실행 중인 경우에만 실행
            self.go_abs_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)
            self.run_recipe_button.config(state=tk.DISABLED)
            self.stop_recipe_button.config(state=tk.DISABLED)
            self.exit_button.config(state=tk.DISABLED)

            self.recipe.stopRecipe()
            print("On stopRecipeButton")

            # Recipe 작업이 완료될 때까지 대기
            while self.recipe.isRunning():
                time.sleep(0.1)  # 일시적으로 대기, 적절한 대기 방법으로 변경 가능

            self.runRecipeEnableButtons()

            self.go_abs_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
            self.run_recipe_button.config(state=tk.NORMAL)
            self.stop_recipe_button.config(state=tk.NORMAL)
            self.exit_button.config(state=tk.NORMAL)

    def closeWindowButton(self):
        self.root.destroy()

    def updateCountLabel(self):
        count_str = str(self.recipe.count).zfill(len(str(self.recipe.csv_size)))
        csv_size_str = str(self.recipe.csv_size)
        formatted_text = f"{count_str} / {csv_size_str}"
        self.recipe_count_label.config(text=formatted_text, justify='center')

if __name__ == "__main__":
    root = tk.Tk()
    app = Window(root)
    root.mainloop()
