import customtkinter
from DONLOD import *
import shutil

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.geometry("800x600")

def donload():
    bid = entry1.get("1.0",'end-1c').split()
    print(bid)
    download(bid)
    print("done donlod")

def zip():
    shutil.make_archive("pool", 'zip', "maps/")


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