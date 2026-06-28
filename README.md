'''pomodoro_timer
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
work_time = 25*60
short_break_time= 5*60
long_break_time = 15*60

class PomodoroTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("200x200")
        self.root.title("Pomodoro Timer")
        self.style = ttk.Style(theme="simplex")

        self.timer_label = tk.Label(self.root, text="25:00", font=("TkDefaultFont", 40))
        self.timer_label.pack(pady=20)

        self.start_button = ttk.Button(self.root, text="Start", command=self.start_timer)
        self.start_button.pack(pady=5)

        self.stop_button = ttk.Button(self.root, text="Stop", command=self.stop_timer,
                                        state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.work_time, self.break_time = work_time, short_break_time
        self.is_work_time, self.pomodoros_completed, self.is_running = True, 0, False

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
                if self.break_time == 0:
                    self.is_work_time, self.work_time = True, work_time
                    messagebox.showinfo("Work Time", " Get back to work!")
            minutes, seconds = divmod(self.work_time if self.is_work_time else self.break_time, 60)
            self.timer_label.config(text="{:02d}:{:02d}".format(minutes, seconds))
            self.root.after(1000, self.update_timer)
PomodoroTimer()

''' notesapp
import tkinter as tk
from tkinter import ttk, messagebox
import json
from tkinter.font import BOLD
from ttkbootstrap import Style

root = tk.Tk()
root.title("Notes App")
root.geometry("500x500")

style = Style(theme='journal')
style.configure("TNotebook.Tab", font=("TkDefaultFont", 14, BOLD))

notes = {}
try:
    with open("notes.json", "r") as f:
        notes = json.load(f)
except FileNotFoundError:
    pass

notebook = ttk.Notebook(root)
notebook.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)


def add_note():
    note_frame = ttk.Frame(notebook, padding=10)
    notebook.add(note_frame, text="New Note")

    title_label = ttk.Label(note_frame, text="Title:")
    title_label.grid(row=0, column=0, padx=10, pady=10)

    title_entry = ttk.Entry(note_frame, width=40)
    title_entry.grid(row=0, column=1, padx=10, pady=10)

    content_label = ttk.Label(note_frame, text="Content:")
    content_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    content_entry = tk.Text(note_frame, width=40, height=10)
    content_entry.grid(row=1, column=1, padx=10, pady=10)

    def save_note():
        title = title_entry.get()
        content = content_entry.get("1.0", tk.END)

        notes[title] = content.strip()

        with open("notes.json", "w") as f:
            json.dump(notes, f)

        note_content = tk.Text(notebook, width=40, height=10)
        note_content.insert(tk.END, content)
        notebook.forget(notebook.select())
        notebook.add(note_content, text=title)

    save_button = ttk.Button(note_frame, text="Save",
                              command=save_note, style="secondary.TButton")
    save_button.grid(row=2, column=1, padx=10, pady=10)


def load_notes():
    global notes
    try:
        with open("notes.json", "r") as f:
            notes = json.load(f)

        for title, content in notes.items():
            note_content = tk.Text(notebook, width=40, height=10)
            note_content.insert(tk.END, content)
            notebook.add(note_content, text=title)

    except FileNotFoundError:
        pass


load_notes()


def delete_notes():
    current_tab = notebook.index(notebook.select())

    note_title = notebook.tab(current_tab, "text")

    confirm = messagebox.askyesno(
        "Delete Note",
        f"Are you sure you want to delete {note_title}?"
    )

    if confirm:
        notebook.forget(current_tab)
        notes.pop(note_title, None)

        with open("notes.json", "w") as f:
            json.dump(notes, f)


new_button = ttk.Button(root, text="New Note",
                         command=add_note, style="info.TButton")
new_button.pack(side=tk.LEFT, padx=10, pady=10)

delete_button = ttk.Button(root, text="Delete",
                            command=delete_notes, style="primary.TButton")
delete_button.pack(side=tk.LEFT, padx=10, pady=10)

root.mainloop()

'''music_player
import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar
import customtkinter as ctk  # type: ignore
from mutagen.mp3 import MP3  # type: ignore
import threading
import pygame
import time
import os

pygame.mixer.init()

current_position = 0
paused = False
selected_folder_path = ""


def update_progress():
    global current_position
    while True:
        if pygame.mixer.music.get_busy() and not paused:
            current_position = pygame.mixer.music.get_pos() / 1000
            pbar["value"] = current_position

            if current_position >= pbar["maximum"]:
                stop_music()
                pbar["value"] = 0

        time.sleep(0.1)


def select_music_folder():
    global selected_folder_path
    selected_folder_path = filedialog.askdirectory()
    if selected_folder_path:
        lbox.delete(0, tk.END)
        for filename in os.listdir(selected_folder_path):
            if filename.endswith(".mp3"):
                lbox.insert(tk.END, filename)


def previous_song():
    if len(lbox.curselection()) > 0:
        current_index = lbox.curselection()[0]
        if current_index > 0:
            lbox.selection_clear(0, tk.END)
            lbox.selection_set(current_index - 1)
            play_selected_song()


def next_song():
    if len(lbox.curselection()) > 0:
        current_index = lbox.curselection()[0]
        if current_index < lbox.size() - 1:
            lbox.selection_clear(0, tk.END)
            lbox.selection_set(current_index + 1)
            play_selected_song()


def play_music():
    global paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        play_selected_song()


def play_selected_song():
    global current_position, paused
    if len(lbox.curselection()) > 0:
        current_index = lbox.curselection()[0]
        selected_song = lbox.get(current_index)
        full_path = os.path.join(selected_folder_path, selected_song)
        current_position = 0
        pygame.mixer.music.load(full_path)
        pygame.mixer.music.play(start=current_position)
        paused = False
        audio = MP3(full_path)
        song_duration = audio.info.length
        pbar["maximum"] = song_duration


def pause_music():
    global paused
    pygame.mixer.music.pause()
    paused = True


def stop_music():
    global paused, current_position
    pygame.mixer.music.stop()
    paused = False
    current_position = 0


window = tk.Tk()
window.title("Music Player App")
window.geometry("600x500")

l_music_player = tk.Label(window, text="Music Player", font=("TkDefaultFont", 30, "bold"))
l_music_player.pack(pady=10)

btn_select_folder = ctk.CTkButton(window, text="Select Music Folder",
                                   command=select_music_folder,
                                   font=("TkDefaultFont", 18))
btn_select_folder.pack(pady=20)

lbox = tk.Listbox(window, width=50, font=("TkDefaultFont", 16))
lbox.pack(pady=10)

btn_frame = tk.Frame(window)
btn_frame.pack(pady=20)

btn_previous = ctk.CTkButton(btn_frame, text="Previous", command=previous_song,
                              width=50, font=("TkDefaultFont", 18))
btn_previous.pack(side=tk.LEFT, padx=5)

btn_play = ctk.CTkButton(btn_frame, text="Play", command=play_music, width=50,
                          font=("TkDefaultFont", 18))
btn_play.pack(side=tk.LEFT, padx=5)

btn_pause = ctk.CTkButton(btn_frame, text="Pause", command=pause_music, width=50,
                           font=("TkDefaultFont", 18))
btn_pause.pack(side=tk.LEFT, padx=5)

btn_next = ctk.CTkButton(btn_frame, text="Next", command=next_song,
                          width=50, font=("TkDefaultFont", 18))
btn_next.pack(side=tk.LEFT, padx=5)

pbar = Progressbar(window, length=300, mode="determinate")
pbar.pack(pady=10)

# Start the progress-update thread only after all widgets exist
pt = threading.Thread(target=update_progress)
pt.daemon = True
pt.start()

window.mainloop()
