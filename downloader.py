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
        self.d_url_list = ["https://api.nerinyan.moe/d/","https://kitsu.moe/d/"]
        self.beatmap_info_url = "https://kitsu.moe/api/b/"

        self.frame = frame

        self.download_in_progress = False

    def update_count(self, count, no_of_maps):
        self.maps_downloaded_label.configure(text=f"Maps downloaded: {count}/{no_of_maps}")
        
    def give_map_not_found_message(self):
        self.maps_downloaded_label.configure(text="Map could not be downloaded.")
        time.sleep(2)
        
    def load_gui_elements(self):
        # Creates progress bar and label to show number of maps downloaded
        self.progress_bar = customtkinter.CTkProgressBar(master = self.frame)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=PAD_Y, padx=10)

        self.maps_downloaded_label = customtkinter.CTkLabel(master=self.frame, text="Maps downloaded: ")
        self.maps_downloaded_label.pack(pady=PAD_Y, padx=10)
    
    def unload_gui_elements(self):
        # Unloads progress bar and label
        self.maps_downloaded_label.destroy()
        self.progress_bar.destroy()

    def convert_to_setid(self, response):
        # Returns setid of a beatmap
        return str(json.loads(response.content)["ParentSetID"])

    def try_to_download_map(self, setid):
        map_not_found_flag = True
        for d_url in self.d_url_list:
            print("tried")
            setid_check_response = requests.get(url=f"{d_url}{setid}")
            print("bruh")
            if setid_check_response.status_code == 200:
                map_not_found_flag = False
                break
        if map_not_found_flag:
            # Then map does not exist
            return None
        return setid_check_response

    def check_if_bid_or_setid(self, map_id):
        """Checks if id is a beatmap ID, set ID, or does not exist. If it exists, function
        returns a response containing map"""

        output_response = None
        bid_check_response = requests.get(url=f"{self.beatmap_info_url}{map_id}")

        if bid_check_response.status_code == 200:
            # Then it is a beatmap id 
            map_id = self.convert_to_setid(bid_check_response)
            output_response = self.try_to_download_map(map_id)
        else:
            output_response = self.try_to_download_map(map_id)
        
        if output_response == None:
            # Then map not available
            self.give_map_not_found_message()
            return None, None
        else:
            # Map has been downloaded
            return output_response, map_id

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
        download_thread = threading.Thread(target=lambda:self.download(bid))
        download_thread.start()
        
    def download(self, bid_list:list):
        """Takes download file path, beatmap ID list, progress bar label and boolean value as parameters.
        If is_beatmap_id is 1, then the function used to download maps using beatmap ID is called,
        else each item in the beatmap ID list is fed to the function used to download maps using
        beatmap set ID"""
        print(bid_list)
        self.load_gui_elements()

        count = 0
        no_of_maps = len(bid_list)
        
        for map_id in bid_list:
            self.update_count(count, no_of_maps)
            response, setid = self.check_if_bid_or_setid(map_id)
            if response != None:
                self.start_download(response, setid)
            count += 1

        self.unload_gui_elements()
        self.download_in_progress = False

    def start_download(self, response, setid):
        chunk_size = 1024
        total = int(response.headers.get('content-length', 0))
        with open (
            f"{DOWNLOAD_DEST_PATH}/{setid}.osz", "wb") as file, tqdm(desc=f"{setid}.osz", 
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
            bar_format='{percentage:3.0f}',
        ) as bar:
            prev_percentage = 0
            current_percentage = 0
            for data in response.iter_content(chunk_size=chunk_size):
                size = file.write(data)
                bar.update(size)
                # Updates percentage bar at every 0.1 interval
                current_percentage = "{:.2f}".format(bar.n/total)
                if prev_percentage != current_percentage:
                    self.progress_bar.set((bar.n/total))
                prev_percentage = current_percentage



