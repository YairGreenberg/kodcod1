<<<<<<< HEAD
from time import strftime
=======
# import keyboard
# booli = True
# while booli:
#     event = keyboard.record(until='hhh555')
#     print(event)
#     if "hhh555" in event:
#         break
# # keyboard.play(event)

# print(list(keyboard.get_typed_strings(event)))





>>>>>>> a48dabe1e800eaaab7ddde845f690aa6fe1f7405
from pynput import keyboard
from datetime import datetime


<<<<<<< HEAD
now = datetime.now()
y = now.strftime('%d/%m/%y %H:%M')
=======

import keyboard

# y = now.strftime('%d/%m/%y %H:%M')

>>>>>>> a48dabe1e800eaaab7ddde845f690aa6fe1f7405
dicti = {}

def append_to_dict(char):
    global dicti,y
    try:
        dicti[y].append(char)
        print(dicti)
    except AttributeError:
        # Handle special keys (e.g., space, enter, shift)
        dicti[y].append(char)
        print(dicti)


def on_key_press(key):
    now = datetime.now().strftime('%d/%m/%y %H:%M')
    global dicti,y
<<<<<<< HEAD
    key = str(key)[14]
    if y in dicti:
        if y == now:
            append_to_dict(key)
        else:
            dicti[now] = []
            append_to_dict(key)
    else:
        dicti[y] = []
        append_to_dict(key)

=======
    if datetime.minute in dicti:
        if datetime.now() == now:
            try:
                dicti[datetime.now()].append(key)
                print(dicti)
            except AttributeError:
                # Handle special keys (e.g., space, enter, shift)
                dicti[datetime.now()].append(key)
                print(dicti)
        else:
            dicti[datetime.now()] = []
            try:
                dicti[datetime.now()].append(key)
                print(dicti)
            except AttributeError:
                # Handle special keys (e.g., space, enter, shift)
                dicti[datetime.now()].append(key)
                print(dicti)
    else:
        dicti[datetime.now()] = []
        try:
            dicti[datetime.now()].append(key)
            print(dicti)
        except AttributeError:
            # Handle special keys (e.g., space, enter, shift)
            dicti[datetime.now()].append(key)
            print(dicti)
>>>>>>> a48dabe1e800eaaab7ddde845f690aa6fe1f7405

# Register the callback function

 # Waits until the 'esc' key is pressed to exit
keyboard.on_press(on_key_press)
keyboard.wait('esc')
print(dicti)
