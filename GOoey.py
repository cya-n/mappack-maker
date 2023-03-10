import customtkinter
import tkinter
from DONLOD import *
import shutil

DOWNLOAD_DEST_PATH = "maps"
ZIPFILE_PATH = "pool"

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.geometry("800x600")

frameCnt = 104
frames = [tkinter.PhotoImage(file='ramez_trans.gif',format = 'gif -index %i' %(i)) for i in range(frameCnt)]

def update(ind):
    global frameCnt
    global label
    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
        ind = 0
    label.configure(image=frame)
    root.after(100, update, ind)

def remove_image():
    global label
    label.configure(image=None)

def donload():
    bid = entry1.get("1.0",'end-1c').split()
    print(bid)
    root.after(0, update, 0)
    download(DOWNLOAD_DEST_PATH, bid)
    remove_image()

    print("done donlod")
    # del loading_screen

def zip():
    shutil.make_archive(ZIPFILE_PATH, 'zip', "maps/")


frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="beatmap donload")
label.pack(pady=12, padx=10)

entry1 = customtkinter.CTkTextbox(master=frame, width=454, height=200)
entry1.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=frame, text="DONLOD", command=donload)
button.pack(pady=12, padx=10)

button2 = customtkinter.CTkButton(master=frame, text="ZIP pls", command=zip)
button2.pack(pady=12, padx=10)

checkbox = customtkinter.CTkCheckBox(master=frame, text = "xd")
checkbox.pack(pady=12, padx=10)    

root.mainloop()