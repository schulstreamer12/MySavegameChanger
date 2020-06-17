from tkinter import *
from tkinter import filedialog, simpledialog
from time import localtime, strftime
import os
import scan
import json

window = Tk()

window.title("Savegame Switcher")
window.iconbitmap("icons/icon.ico")
window.geometry("1100x650")
#window.resizable(width=0, height=0)

pathes = {}

def log_post(message):
    text_log.config(state="normal")

    time = strftime("%H:%M:%S: ",localtime())

    message = time + message + "\n"

    text_log.insert(END, message)
    text_log.see(END)
    text_log.config(state=DISABLED)

def log_clear():
    text_log.config(state="normal")
    text_log.delete(1.0,END)
    text_log.config(state=DISABLED)

def save():
    print("save")

#frames
frame_lettering = Frame(master=window, )#bg="red")
frame_lettering.place(x=0, y=0, width=1100, height=50)

frame_listboxes = Frame(master=window, )#bg="blue")
frame_listboxes.place(x=0, y=50, width=1100, height=400)

frame_log = Frame(master=window, )#bg="green")
frame_log.place(x=0, y=450, width=800, height=200)

#frame lettering
label_active_savegame = Label(master=frame_lettering, text="Active savegame")
label_active_savegame.place(x=30, y=25)

label_passive_savegame = Label(master=frame_lettering, text="Passive savegames")
label_passive_savegame.place(x=400, y=25)

label_savegame_name = Label(master=frame_lettering, text="Here will stand the name of your selected safegame!")
label_savegame_name.place(x=720, y=5)

label_description = Label(master=frame_lettering, text="Description:")
label_description.place(x=720, y=25)

def rename_savegame():
    new_name = simpledialog.askstring("Rename selected savegame", "Please enter new name:")
    label_savegame_name.config(text=new_name)

button_rename_savegame = Button(master=frame_lettering, text="Rename", command=rename_savegame)
button_rename_savegame.place(x=1000, y=5, height=25)

#frame listboxes
listbox_left = Listbox(master=frame_listboxes)
listbox_left.place(x=30, y=0, width=300, height=350)

listbox_right = Listbox(master=frame_listboxes)
listbox_right.place(x=400, y=0, width=300, height=350)

text_description = Text(master=frame_listboxes)
text_description.place(x=720, y=0, width=320, height=350)

scrollbar_description = Scrollbar(master=frame_listboxes)
scrollbar_description.place(x=1040, y=0, height=350)

scrollbar_description.config(command=text_description.yview)
text_description.config(yscrollcommand= scrollbar_description.set)

def listbox_left_selected(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    
    label_savegame_name.config(text=value)
    pathes[value]

def listbox_right_selected(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    
    label_savegame_name.config(text=value)

listbox_left.bind('<<ListboxSelect>>', listbox_left_selected) #bind: when you select a item the function will start
listbox_right.bind('<<ListboxSelect>>', listbox_right_selected)

def save_name_desc():
    new_name = label_savegame_name.cget("text") #get name
    new_description = text_description.get("1.0",'end-1c') #get description

    left = listbox_left.curselection()
    right = listbox_right.curselection()
    
    if listbox_left.get(ANCHOR) != "": #try to get out of the selected item the slected anchor
        anchor = listbox_left.get(ANCHOR)
    elif listbox_right.get(ANCHOR) != "":
        anchor = listbox_right.get(ANCHOR)

    pathes[new_name] = pathes.pop(anchor)

    if right != "": #decide what listbox is selected, to make the new name visible in the listboxes
        listbox_right.delete(right)
        size = listbox_right.size()
        listbox_right.insert(right, new_name)
    elif left != "":
        listbox_left.delete(left)
        size = listbox_left.size()
        listbox_left.insert(left, new_name)

    path = pathes[new_name]["path"]
    for_json = {"name" : new_name, "description" : new_description} #make the dictonary that we store

    with open("sample.json", "w") as outfile: #save as json in savegame folder
        json.dump(for_json, outfile, indent=4)

button_save = Button(master=frame_listboxes, text="Save name and description!", command=save_name_desc)
button_save.place(x=720, y=360)

copy_in_appdata = ""
copy_out_appdata = ""

def move_right():
    print("Left to right")
    number = listbox_left.curselection()
    name = listbox_left.get(ANCHOR)
    print(name)
    listbox_left.delete(number)
    size = listbox_right.size()
    listbox_right.insert(size, name)
    #need to put in variable what you need to copy!

def move_left():
    print("Right to left")
    number = listbox_right.curselection()
    name = listbox_right.get(ANCHOR)
    print(name)
    listbox_right.delete(number)
    size = listbox_left.size()
    listbox_left.insert(size, name)

button_left = Button(master=frame_listboxes, text="<", command=move_left)
button_left.place(x=355, y=0)

button_right = Button(master=frame_listboxes, text=">", command=move_right)
button_right.place(x=355, y=30)

button_save = Button(master=frame_listboxes, text="Save this!", command=save)
button_save.place(x=400, y=360)

#frame log
label_lettering_log = Label(master=frame_log, text="Log:")
label_lettering_log.place(x=30, y=0)

button_delete_log = Button(master=frame_log, text="delete", command=log_clear)
button_delete_log.place(x=610, y=0, width=80, height=20)

text_log = Text(master=frame_log, state=DISABLED) #to write in the textbox: state:normal>insert>state:disable
text_log.place(x=30, y=25, width=650, height=125)

scrollbar_log = Scrollbar(master=frame_log)
scrollbar_log.place(x=675, y=25, height=125)

scrollbar_log.config(command=text_log.yview)
text_log.config(yscrollcommand= scrollbar_log.set)

def savegame_start_scan():
    storage = []
    storage = scan.scan("savegames")

    for items in storage:
        log_post("Found savegame: " + items)
        listbox_right.insert(0, items)
        
        path = os.path.join("savegames" , items)

        properties = {"path" : path}
        pathes[items] = properties

    path = os.path.join("C:\\","Users",os.getlogin(),"AppData","LocalLow","Amistech")
    log_post("Get savegame path: " + path)

    savegames = []
    savegames = scan.scan(path)

    for items in savegames:
        log_post("Found savegame: " + items)

        if items == "My Summer Car":
            listbox_left.insert(0, items)
        else:
            listbox_right.insert(0, items)
        
        path_savegame = os.path.join("C:\\","Users",os.getlogin(),"AppData","LocalLow","Amistech",items)
        properties = {"path" : path_savegame}
        pathes[items] = properties
        
    print(pathes)

savegame_start_scan()
log_post("Savegame Switcher started!")

window.mainloop()
