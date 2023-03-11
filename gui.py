import customtkinter
from downloader import *
import shutil
import threading

#COMMON USE VARIABLES
DOWNLOAD_DEST_PATH = "maps/"
ZIPFILE_PATH = "pool/"
PAD_Y = 8

# Setting up window
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

class Gui:
    def __init__(self):
        self.root = customtkinter.CTk()
        self.root.geometry("1024x768")
        self.root.title("beatmap-downloader")

        # Frame object, contains all the elements of the app
        self.frame = customtkinter.CTkFrame(master=self.root)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        # Beatmap ID label and entry
        self.enter_bid_label = customtkinter.CTkLabel(master=self.frame, text="Enter beatmap IDs:")
        self.enter_bid_label.pack(pady=PAD_Y, padx=10)

        self.bid_entry = customtkinter.CTkTextbox(master=self.frame, width=454, height=150)
        self.bid_entry.pack(pady=PAD_Y, padx=10)

        # Download path label and entry
        self.download_path_label = customtkinter.CTkLabel(master=self.frame, text="Download path (File that gets zipped): ")
        self.download_path_label.pack(pady=PAD_Y, padx=10)

        # Inserts placeholder text in the entry
        self.download_path_entry = customtkinter.CTkTextbox(master=self.frame, width=454, height=20)
        self.download_path_entry.insert("0.0", DOWNLOAD_DEST_PATH)
        self.download_path_entry.pack(pady=PAD_Y, padx=10)

        # Zipfile path label and entry
        self.zip_path_label = customtkinter.CTkLabel(master=self.frame, text="Zip destination: ")
        self.zip_path_label.pack(pady=PAD_Y, padx=10)

        self.zip_path_entry = customtkinter.CTkTextbox(master=self.frame, width=454, height=20)
        self.zip_path_entry.insert("0.0", ZIPFILE_PATH)
        self.zip_path_entry.pack(pady=PAD_Y, padx=10)

        # Download button, calls the initialize download function
        self.download_button = customtkinter.CTkButton(master=self.frame, text="DONLOAD", command=self.initialize_download)
        self.download_button.pack(pady=PAD_Y, padx=10)

        # Initialise downloader object
        self.downloader = Downloader(self.frame)
        
        # Zip button, zips the download file and stores it in specified location
        self.zip_button = customtkinter.CTkButton(master=self.frame, text="Create .zip", command=self.zip_download_file)
        self.zip_button.pack(pady=PAD_Y, padx=10)

        self.root.mainloop()

    def initialize_download(self):
        """Called by the download button. Gets beatmap IDs, download destination path and zipfile path from the entries and calls the download function"""
        # Get values from entries
        DOWNLOAD_DEST_PATH = self.download_path_entry.get("1.0", "end-1c")
        ZIPFILE_PATH = self.zip_path_entry.get("1.0", "end-1c")
        bid = list(set(self.bid_entry.get("1.0",'end-1c').split()))

        # Initialises download thread to prevent freezing the window during download
        download_thread = threading.Thread(target=lambda:self.downloader.download(DOWNLOAD_DEST_PATH, bid))
        download_thread.start()

    def zip_download_file(self):
        """Called by the zip button. Zips the download destination file at the zipfile path"""

        # Initialises zip thread to prevent freezing the window during zipping
        zip_thread = threading.Thread(target=lambda:shutil.make_archive(ZIPFILE_PATH, 'zip', DOWNLOAD_DEST_PATH))
        zip_thread.start()