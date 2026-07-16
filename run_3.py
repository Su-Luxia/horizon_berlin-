import subprocess
import os
import sys

venv_python = r"a:\Computer\Alla\HackClub\horizon_berlin-\zelda\.venv\Scripts\python.exe"

scripts = [
    "music_player.py",
    "pomodoro_timer.py",
    "notesapp.py"
]

processes = []
for script in scripts:
    if os.path.exists(script):
        proc = subprocess.Popen([venv_python, script])
        processes.append(proc)
    else:
        print("Error")

try:
    for proc in processes:
        proc.wait()
except KeyboardInterrupt:
    for proc in processes:
        proc.terminate()