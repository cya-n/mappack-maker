import customtkinter
import tkinter
from DONLOD import *
import shutil
import threading
from PIL import Image

DOWNLOAD_DEST_PATH = "maps/"
ZIPFILE_PATH = "pool/"
PAD_Y = 8

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.geometry("1024x768")

def donload():
    DOWNLOAD_DEST_PATH = download_path_entry.get("1.0", "end-1c")
    ZIPFILE_PATH = zip_path_entry.get("1.0", "end-1c")
    bid = set(entry1.get("1.0",'end-1c').split())

    prog_bar = customtkinter.CTkLabel(master = frame, text="")
    prog_bar.pack(pady=PAD_Y, padx=10)

    download_thread = threading.Thread(target=lambda:download(DOWNLOAD_DEST_PATH, bid, prog_bar, radio_var.get()))
    download_thread.start()

def zip():
    zip_thread = threading.Thread(target=lambda:shutil.make_archive(ZIPFILE_PATH, 'zip', "maps/"))
    zip_thread.start()

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Enter beatmap IDs:")
label.pack(pady=PAD_Y, padx=10)

entry1 = customtkinter.CTkTextbox(master=frame, width=454, height=150)
entry1.pack(pady=PAD_Y, padx=10)

download_path_label = customtkinter.CTkLabel(master=frame, text="Download path (File that gets zipped): ")
download_path_label.pack(pady=PAD_Y, padx=10)

download_path_entry = customtkinter.CTkTextbox(master=frame, width=454, height=20)
download_path_entry.insert("0.0", DOWNLOAD_DEST_PATH)
download_path_entry.pack(pady=PAD_Y, padx=10)

zip_path_label = customtkinter.CTkLabel(master=frame, text="Zip destination: ")
zip_path_label.pack(pady=PAD_Y, padx=10)

zip_path_entry = customtkinter.CTkTextbox(master=frame, width=454, height=20)
zip_path_entry.insert("0.0", ZIPFILE_PATH)
zip_path_entry.pack(pady=PAD_Y, padx=10)

button = customtkinter.CTkButton(master=frame, text="DONLOD", command=donload)
button.pack(pady=PAD_Y, padx=10)

radio_var = customtkinter.IntVar()

def radiobutton_event():
    print("radiobutton toggled, current value:", radio_var.get())

setid_button = customtkinter.CTkRadioButton(master=frame, text="Set ID",
                                             command=radiobutton_event, variable= radio_var, value=0)
beatmapid_button = customtkinter.CTkRadioButton(master=frame, text="Beatmap ID",
                                             command=radiobutton_event, variable= radio_var, value=1)
setid_button.select()
setid_button.pack(padx=20, pady=PAD_Y)
beatmapid_button.pack(padx=20, pady=PAD_Y)

button2 = customtkinter.CTkButton(master=frame, text="ZIP pls", command=zip)
button2.pack(pady=PAD_Y, padx=10)

root.mainloop()