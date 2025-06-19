import keyboard
# import prodect_keylogger as pk
def on_key_press(key):
    print(key)
keyboard.on_press(on_key_press)

keyboard.wait('Ctrl + Shift + .')