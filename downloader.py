import customtkinter
import json
import requests
import time
from tqdm import tqdm

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
        

    def download_beatmap_id(self, file_path, bid_list):
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
        

    def download_set_id(self, file_path, setID, chunk_size=1024):
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
        



