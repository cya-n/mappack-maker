import customtkinter
import json
import requests
import threading
import time
from tqdm import tqdm
import os
import re

#COMMON USE VARIABLES
DOWNLOAD_DEST_PATH = "maps/"
ZIPFILE_PATH = "pool/"
PAD_Y = 8

class Downloader:
    def __init__(self, frame):
        self.d_url_list = ["https://kitsu.moe/d/", "https://api.nerinyan.moe/d/"]
        self.beatmap_info_url = "https://kitsu.moe/api/b/"

        self.frame = frame
        self.radio_var = customtkinter.IntVar()

        self.beatmapid_button = customtkinter.CTkRadioButton(master=self.frame, text="Beatmap ID", variable= self.radio_var, value=1)
        self.setid_button = customtkinter.CTkRadioButton(master=self.frame, text="Set ID", variable= self.radio_var, value=0)
        self.beatmapid_button.select()
        self.beatmapid_button.pack(padx=20, pady=PAD_Y)
        self.setid_button.pack(padx=20, pady=PAD_Y)

        self.download_in_progress = False

    def get_beatmap_set_ids_from_text(text):
        # Regex to find set ID from beatmapset link
        regex_beatmapset_id = re.compile("(?<=beatmapsets\/)([0-9]*)", re.MULTILINE) # matches format /beatmapsets/xxxxx#xxxxx (setID#difficultyID) or /beatmapsets/xxxxx (setID)
       
        # Regex to find difficultyID links
        regex_difficulty_id_link = re.compile("(.*\/(b|beatmaps)\/.*)", re.MULTILINE) # matches format /b/xxxxx or /beatmaps/xxxxx (difficulty id)

        # Regex to find difficultyIDs
        regex_difficulty_id = re.compile("^[0-9]+$", re.MULTILINE) # matches format xxxxx (difficulty id)
        
        # Add all setIDs from links
        set_ids = []
        for i in re.findall(regex_beatmapset_id, text):
            set_ids.append(i)

        # Get setIDs from difficultyID links
        for match in re.findall(regex_difficulty_id_link, text):
            url = match[0]
            try:
                r = requests.head(url, allow_redirects=True, timeout=10)

                set_ids.append(re.findall(regex_beatmapset_id, r.url)[0])
            except:
                print("{} is not a valid beatmap URL!".format(url))

        # Get setIDs from difficultyIDs
        for difficulty_id in re.findall(regex_difficulty_id, text):
            prefix = "https://osu.ppy.sh/b/"
            url = prefix + difficulty_id

            try:
                r = requests.head(url, allow_redirects=True, timeout=10)
                set_ids.append(re.findall(regex_beatmapset_id, r.url)[0])
            except:
                print("{} is not a valid beatmap URL!".format(url))

        return set_ids

    def initialize_download(self, gui):
        """Called by the download button. Gets beatmap IDs, download destination path and zipfile path from the entries and calls the download function"""
        # if the function is currently executing, the download wont start
        if self.download_in_progress:
            return
        self.download_in_progress = True
        # Get values from entries
        DOWNLOAD_DEST_PATH = gui.download_path_entry.get("1.0", "end-1c")
        if not os.path.exists(DOWNLOAD_DEST_PATH):
            os.makedirs(DOWNLOAD_DEST_PATH)
        ZIPFILE_PATH = gui.zip_path_entry.get("1.0", "end-1c")
        bid = list(set(gui.bid_entry.get("1.0",'end-1c').split()))

        # Initialises download thread to prevent freezing the window during download
        download_thread = threading.Thread(target=lambda:self.download(DOWNLOAD_DEST_PATH, bid))
        download_thread.start()

    def download(self, file_path:str, bid_list:list):
        """Takes download file path, beatmap ID list, progress bar label and boolean value as parameters.
        If is_beatmap_id is 1, then the function used to download maps using beatmap ID is called,
        else each item in the beatmap ID list is fed to the function used to download maps using
        beatmap set ID"""
        # Creates progress bar and label to show number of maps downloaded
        self.progress_bar = customtkinter.CTkProgressBar(master = self.frame)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=PAD_Y, padx=10)

        self.maps_downloaded_label = customtkinter.CTkLabel(master=self.frame, text="Maps downloaded: ")
        self.maps_downloaded_label.pack(pady=PAD_Y, padx=10)

        is_beatmap_id = self.radio_var.get()
        if is_beatmap_id:
            self.download_beatmap_id(file_path, bid_list)
        else:
            count = 0
            no_of_maps = len(bid_list)
            for bid in bid_list:
                self.maps_downloaded_label.configure(text=f"Maps downloaded: {count}/{no_of_maps}")
                self.download_set_id(file_path, bid)
                count += 1

        self.maps_downloaded_label.destroy()
        self.progress_bar.destroy()

        self.download_in_progress = False

    def download_beatmap_id(self, file_path:str, bid_list:list):
        """Uses kitsune's beatmap info api to get the beatmap set ID using the beatmap IDs in the beatmap 
        ID list using for loop. This beatmap set ID is fed to the beatmap set ID download function."""
        count = 0
        no_of_maps = len(bid_list)
        for _ in bid_list:
            self.maps_downloaded_label.configure(text=f"Maps downloaded: {count}/{no_of_maps}")
            response = requests.get(self.beatmap_info_url+bid_list[count])
            setID = str(json.loads(response.content)["ParentSetID"])
            self.download_set_id(file_path, setID)
            count+=1

    def download_set_id(self, file_path:str, setID:int, chunk_size=1024):
        """Uses kitsune's beatmap set downloader api to download .osz file and store it in the download file
        . Also implements the progress bar using tqdm."""
        map_not_found = True
        for d_url in self.d_url_list:
            response2 = requests.get(d_url+setID)
            if response2.status_code == 200:
                map_not_found = False
                break

        if map_not_found:
            self.maps_downloaded_label.configure(text=f"Map {setID} does not exist, try changing ID type.")
            time.sleep(2)
            return

        total = int(response2.headers.get('content-length', 0))
        with open (
            f"{file_path}/{setID}.osz", "wb") as file, tqdm(desc=f"{setID}.osz", 
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
            bar_format='{percentage:3.0f}',
        ) as bar:
            prev_percentage = 0
            current_percentage = 0
            for data in response2.iter_content(chunk_size=chunk_size):
                size = file.write(data)
                bar.update(size)
                # Updates percentage bar at every 0.01 interval
                current_percentage = "{:.2f}".format(bar.n/total)
                if prev_percentage != current_percentage:
                    self.progress_bar.set((bar.n/total))
                prev_percentage = current_percentage
        



