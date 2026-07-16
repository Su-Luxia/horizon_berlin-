import subprocess
import os
import sys

venv_python = r"a:\Computer\Alla\HackClub\horizon_berlin-\zelda\.venv\Scripts\python.exe"

scripts = [
    {
        "path": r"a:\Computer\Alla\HackClub\horizon_berlin-\music_player.py", 
        "cwd": None
    },
    {
        "path": r"a:\Computer\Alla\HackClub\horizon_berlin-\pomodoro_timer.py", 
        "cwd": None
    },
    {
        "path": r"a:\Computer\Alla\HackClub\horizon_berlin-\notesapp.py", 
        "cwd": None
    },
    {
        "path": r"a:\Computer\Alla\HackClub\horizon_berlin-\PlatformGame\platformer.py", 
        "cwd": r"a:\Computer\Alla\HackClub\horizon_berlin-\PlatformGame" 
    }
]

processes = []
for item in scripts:
    script_path = item["path"]
    working_dir = item["cwd"]
    
    if os.path.exists(script_path):
        proc = subprocess.Popen([venv_python, script_path], cwd=working_dir)
        processes.append(proc)
    else:
        print("Error")

try:
    for proc in processes:
        proc.wait()
except KeyboardInterrupt:
    for proc in processes:
        proc.terminate()