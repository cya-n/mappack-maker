import customtkinter
from DONLOD import *
import shutil
import threading
from PIL import Image

DOWNLOAD_DEST_PATH = "maps"
ZIPFILE_PATH = "pool"

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.geometry("1024x768")

frameCnt = 104
#frames = customtkinter.CTkImage(Image.open('rameez.png'),size=(80,50))


def donload():
    # button.configure(text="",image=frames)
   # rameez = customtkinter.CTkLabel(master=frame, image=frames, text="",height=80,width=50)
   # rameez.pack(pady=12,padx=10)
    global donload_thread
    bid = entry1.get("1.0",'end-1c').split()
    prog_bar = customtkinter.CTkLabel(master = frame, text="")
    prog_bar.pack(pady=12, padx=10)

    download_thread = threading.Thread(target=lambda:download(DOWNLOAD_DEST_PATH, bid, prog_bar))
    download_thread.start()
    

    print("done donlod")
    donload_thread = threading.Thread(target=donload)

def zip():
    zip_thread = threading.Thread(target=lambda:shutil.make_archive(ZIPFILE_PATH, 'zip', "maps/"))
    zip_thread.start()

zip_thread = threading.Thread(target=zip)

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="beatmap donload")
label.pack(pady=12, padx=10)

entry1 = customtkinter.CTkTextbox(master=frame, width=454, height=200)
entry1.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=frame, text="DONLOD", command=donload, height=100,width=120)
button.pack(pady=12, padx=10)

button2 = customtkinter.CTkButton(master=frame, text="ZIP pls", command=zip)
button2.pack(pady=12, padx=10)

checkbox = customtkinter.CTkCheckBox(master=frame, text = "xd")
checkbox.pack(pady=12, padx=10)    

root.mainloop()