import customtkinter
from DONLOD import *
import shutil
import threading

#COMMON USE VARIABLES
DOWNLOAD_DEST_PATH = "maps/"
ZIPFILE_PATH = "pool/"
PAD_Y = 8

# Setting up window
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.geometry("1024x768")
root.title("beatmap-downloader")


def initialize_download():
    """Called by the download button. Gets beatmap IDs, download destination path and zipfile path from the entries and calls the download function"""

    DOWNLOAD_DEST_PATH = download_path_entry.get("1.0", "end-1c")
    ZIPFILE_PATH = zip_path_entry.get("1.0", "end-1c")
    bid = list(set(bid_entry.get("1.0",'end-1c').split()))
    prog_bar = customtkinter.CTkProgressBar(master = frame)
    prog_bar.set(0)
    prog_bar.pack(pady=PAD_Y, padx=10)

    maps_downloaded_label = customtkinter.CTkLabel(master=frame, text="Maps downloaded: ")
    maps_downloaded_label.pack(pady=PAD_Y, padx=10)

    # Initialises download thread to prevent freezing the window during download
    download_thread = threading.Thread(target=lambda:download(DOWNLOAD_DEST_PATH, bid, prog_bar, maps_downloaded_label, radio_var.get()))
    download_thread.start()

def zip_download_file():
    """Called by the zip button. Zips the download destination file at the zipfile path"""

    # Initialises zip thread to prevent freezing the window during zipping
    zip_thread = threading.Thread(target=lambda:shutil.make_archive(ZIPFILE_PATH, 'zip', DOWNLOAD_DEST_PATH))
    zip_thread.start()

# Frame object, contains all the elements of the app
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

# Beatmap ID label and entry
enter_bid_label = customtkinter.CTkLabel(master=frame, text="Enter beatmap IDs:")
enter_bid_label.pack(pady=PAD_Y, padx=10)

bid_entry = customtkinter.CTkTextbox(master=frame, width=454, height=150)
bid_entry.pack(pady=PAD_Y, padx=10)

# Download path label and entry
download_path_label = customtkinter.CTkLabel(master=frame, text="Download path (File that gets zipped): ")
download_path_label.pack(pady=PAD_Y, padx=10)

# Inserts placeholder text in the entry
download_path_entry = customtkinter.CTkTextbox(master=frame, width=454, height=20)
download_path_entry.insert("0.0", DOWNLOAD_DEST_PATH)
download_path_entry.pack(pady=PAD_Y, padx=10)

# Zipfile path label and entry
zip_path_label = customtkinter.CTkLabel(master=frame, text="Zip destination: ")
zip_path_label.pack(pady=PAD_Y, padx=10)

zip_path_entry = customtkinter.CTkTextbox(master=frame, width=454, height=20)
zip_path_entry.insert("0.0", ZIPFILE_PATH)
zip_path_entry.pack(pady=PAD_Y, padx=10)

# Download button, calls the initialize download function
download_button = customtkinter.CTkButton(master=frame, text="DONLOAD", command=initialize_download)
download_button.pack(pady=PAD_Y, padx=10)

# Radio buttons to specify whether the IDs provided are beatmap IDs or beatmap SET IDs. Beatmap ID is selected by default as it is commonly used in tourneys
radio_var = customtkinter.IntVar()

beatmapid_button = customtkinter.CTkRadioButton(master=frame, text="Beatmap ID", variable= radio_var, value=1)
setid_button = customtkinter.CTkRadioButton(master=frame, text="Set ID", variable= radio_var, value=0)
beatmapid_button.select()
beatmapid_button.pack(padx=20, pady=PAD_Y)
setid_button.pack(padx=20, pady=PAD_Y)

zip_button = customtkinter.CTkButton(master=frame, text="Create .zip", command=zip_download_file)
zip_button.pack(pady=PAD_Y, padx=10)

root.mainloop()