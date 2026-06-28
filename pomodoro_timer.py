import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import ttk, Style
work_time = 25*60
short_break_time= 5*60
long_break_time = 15*60

class PomodoroTimer:
    def __init__(self):
        self.root = tk.Tk ()
        self.root.geometry("200x200")
        self.root.title("Pomodoro Timer")
        self.style = Style (theme = "simplex")
        self.style.theme_use()

        self.timer_label = tk.Label(self.root, text="", font=("TkDefaultFont", 40))
        self.timer_label.pack(pady=20)

        self.start_button = ttk.Button(self.root, text="Start", command=self.start_timer)
        self.start_button.pack(pady=5)

        self.start_button = ttk.Button(self.root, text="Stop", command=self.stop_timer,
                                        state=tk.DISABLED)
        self.start_button.pack(pady=5)

        self.work_time, self.break_time = work_time, short_break_time
        self.is_work_time, self.pomodoros_completed, self.is_running = True,0,False

        self.root.mainloop()

    def start_timer(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.is_running = True
        self.update_timer()

    def stop_timer(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.is_running = False
        
    def update_timer(self):
        if self.is_running:
            if self.is_work_time:
                self.work_time -=1
                if self.work_time==0:
                    self.is_work_time = False
                    self.pomodoros_completed += 1 
                    self.break_time = long_break_time if self.pomodoros_completed % 4 == 0 else short_break_time
                    messagebox.showinfo("Great job!" if self.pomodoros_completed % 4 ==0
                                        else "Good job!", "Take a long break and rest"
                                        if self.pomodoros_completed % 4 == 0
                                        else "Take a short break and stretch your legs!")
                    
            else:
                self.break_time -= 1
                if self.break_time:
