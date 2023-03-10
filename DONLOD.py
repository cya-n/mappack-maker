import requests
import time
import json
from tqdm import tqdm

url = "https://kitsu.moe/api/b/"
d_url = "https://kitsu.moe/d/"
# id = input("Enter beatmap id: ").split()

def download(file_path, bid, chunk_size=1024):
    count = 0
    for _ in bid:
        response = requests.get(url+bid[count])
        setID = str(json.loads(response.content)["ParentSetID"])
        response2 = requests.get(d_url+setID)
        total = int(response2.headers.get('content-length', 0))
        #open(f"{file_path}/{setID}.osz", "wb").write(response2.content)
        with open(f"{file_path}/{setID}.osz", "wb") as file, tqdm(desc=f"{file_path}/{setID}.osz",
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,) as bar:
            for data in response2.iter_content(chunk_size=chunk_size):
                size = file.write(data)
                bar.update(size)
                print(bar)
                
        print(f"done donwloading {setID}")
        count+=1


    

# def download(bid):
#     count = 0
#     for _ in bid:
#         response = requests.get(url+bid[count])
#         open(f"maps/{bid[count]}.osz", "wb").write(response.content)
#         print(f"done donloading {bid[count]}")
#         time.sleep(5)
#         count +=1

