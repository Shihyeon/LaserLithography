from src.Controller.motor import Motor
import tkinter as tk

class MotorControlWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Motor Control")
        
        # Motor 객체 생성
        self.motor = Motor()
        
        # X 좌표 입력 필드와 레이블
        self.x_label = tk.Label(self.root, text="X Coord:")
        self.x_label.grid(row=0, column=0)
        self.x_entry = tk.Entry(self.root, width=10)
        self.x_entry.grid(row=0, column=1)
        
        # Y 좌표 입력 필드와 레이블
        self.y_label = tk.Label(self.root, text="Y Coord:")
        self.y_label.grid(row=1, column=0)
        self.y_entry = tk.Entry(self.root, width=10)
        self.y_entry.grid(row=1, column=1)
        
        # 이동 버튼
        move_button = tk.Button(self.root, text="Move X", command=self.move_x)
        move_button.grid(row=2, column=0)
        
        move_y_button = tk.Button(self.root, text="Move Y", command=self.move_y)
        move_y_button.grid(row=2, column=1)
        
        # X 및 Y 축에 대한 경고 메시지 표시 레이블
        self.x_warning_label = tk.Label(self.root, text="", fg="red")
        self.x_warning_label.grid(row=3, column=0, columnspan=2)
        self.y_warning_label = tk.Label(self.root, text="", fg="red")
        self.y_warning_label.grid(row=4, column=0, columnspan=2)
        
        # 종료 버튼
        exit_button = tk.Button(self.root, text="Exit", command=self.exit_program)
        exit_button.grid(row=5, column=0, columnspan=2)
    
    # def move(self):
    #     a = 1
    
    def move_x(self):
        try:
            # X 좌표 입력 필드에서 값을 가져옴
            x_input = self.x_entry.get()
            
            if not x_input:
                return  # 입력이 없는 경우 아무 작업도 수행하지 않음
            
            x_pos = int(x_input)
            
            # X 축 리미트 스위치 상태 확인
            x_limit_status = self.motor.writeAndGetResponse("axi1:limit?")
            
            if x_limit_status != '0':
                # X 축 리미트 스위치가 활성화된 경우
                self.x_warning_label.config(text="X Axis limit switch is enabled.")
            else:
                self.x_warning_label.config(text="")
            
            if x_limit_status == '0':
                # X 축 리미트 스위치가 비활성화된 경우
                # Motor 객체를 사용하여 X 축으로 이동
                self.motor.goAbs(x_pos, 0)
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def move_y(self):
        try:
            # Y 좌표 입력 필드에서 값을 가져옴
            y_input = self.y_entry.get()
            
            if not y_input:
                return  # 입력이 없는 경우 아무 작업도 수행하지 않음
            
            y_pos = int(y_input)
            
            # Y 축 리미트 스위치 상태 확인
            y_limit_status = self.motor.writeAndGetResponse("axi2:limit?")
            
            if y_limit_status != '0':
                # Y 축 리미트 스위치가 활성화된 경우
                self.y_warning_label.config(text="Y Axis limit switch is enabled.")
            else:
                self.y_warning_label.config(text="")
            
            if y_limit_status == '0':
                # Y 축 리미트 스위치가 비활성화된 경우
                # Motor 객체를 사용하여 Y 축으로 이동
                self.motor.goAbs(0, y_pos)
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def exit_program(self):
        # Motor 객체를 닫고 프로그램 종료
        self.motor.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MotorControlWindow(root)
    root.mainloop()
