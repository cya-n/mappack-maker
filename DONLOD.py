import requests
import time
import json
from tqdm import tqdm

url = "https://kitsu.moe/api/b/"
d_url = "https://kitsu.moe/d/"
# id = input("Enter beatmap id: ").split()


def download_beatmap_id(file_path, bid_list, label):
    count = 0
    for _ in bid_list:
        response = requests.get(url+bid_list[count])
        setID = str(json.loads(response.content)["ParentSetID"])
        download_set_id(file_path, setID, label)
        count+=1

def download_set_id(file_path, setID, label, chunk_size=1024):
    response2 = requests.get(d_url+setID)
    total = int(response2.headers.get('content-length', 0))
    with open(f"{file_path}/{setID}.osz", "wb") as file, tqdm(desc=f"{setID}.osz",
    total=total,
    unit='iB',
    unit_scale=True,
    unit_divisor=1024,
    bar_format='{desc} | {percentage:3.0f}%|{bar:15}{r_bar}',) as bar:
        for data in response2.iter_content(chunk_size=chunk_size):
            size = file.write(data)
            bar.update(size)
            label.configure(text=bar)
    
    print(f"done donwloading {setID}")
    

def download(file_path, bid_list, label, is_beatmap_id):
    if is_beatmap_id:
        download_beatmap_id(file_path, bid_list, label)
    else:
        for bid in bid_list:
            download_set_id(file_path, bid, label)
    


    

# def download(bid):
#     count = 0
#     for _ in bid:
#         response = requests.get(url+bid[count])
#         open(f"maps/{bid[count]}.osz", "wb").write(response.content)
#         print(f"done donloading {bid[count]}")
#         time.sleep(5)
#         count +=1

