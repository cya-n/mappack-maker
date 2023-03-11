import requests
import time
import json
from tqdm import tqdm


url = "https://kitsu.moe/api/b/"
d_url = "https://kitsu.moe/d/"


def download(file_path:str, bid_list:list, progress_bar, maps_downloaded_label, is_beatmap_id:int):
    """Takes download file path, beatmap ID list, progress bar label and boolean value as parameters.
    If is_beatmap_id is 1, then the function used to download maps using beatmap ID is called,
    else each item in the beatmap ID list is fed to the function used to download maps using
    beatmap set ID"""

    if is_beatmap_id:
        download_beatmap_id(file_path, bid_list, progress_bar, maps_downloaded_label)
    else:
        count = 0
        for bid in bid_list:
            maps_downloaded_label.configure(text=f"Maps downloaded: {count}/{no_of_maps}")
            download_set_id(file_path, bid, progress_bar, maps_downloaded_label)
            count += 1
    maps_downloaded_label.destroy()
    progress_bar.destroy()
    

def download_beatmap_id(file_path, bid_list, progress_bar, maps_downloaded_label):
    """Uses kitsune's beatmap info api to get the beatmap set ID using the beatmap IDs in the beatmap 
    ID list using for loop. This beatmap set ID is fed to the beatmap set ID download function."""
    count = 0
    no_of_maps = len(bid_list)
    for _ in bid_list:
        maps_downloaded_label.configure(text=f"Maps downloaded: {count}/{no_of_maps}")
        response = requests.get(url+bid_list[count])
        setID = str(json.loads(response.content)["ParentSetID"])
        download_set_id(file_path, setID, progress_bar, maps_downloaded_label)
        count+=1
    

def download_set_id(file_path, setID, progress_bar, maps_downloaded_label, chunk_size=1024):
    """Uses kitsune's beatmap set downloader api to download .osz file and store it in the download file
    . Also implements the progress bar using tqdm."""
    response2 = requests.get(d_url+setID)
    total = int(response2.headers.get('content-length', 0))
    print(total)
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
            # Updates percentage bar at every 0.01 interval to increase speed
            current_percentage = "{:.2f}".format(bar.n/total)
            if prev_percentage != current_percentage:
                progress_bar.set((bar.n/total))
            prev_percentage = current_percentage
    
    print(f"done donwloading {setID}")



