import requests
import time
import json
url = "https://kitsu.moe/api/b/"
d_url = "https://kitsu.moe/d/"
# id = input("Enter beatmap id: ").split()

def download(bid):
    count = 0
    for _ in bid:
        response = requests.get(url+bid[count])
        setID = str(json.loads(response.content)["ParentSetID"])
        response2 = requests.get(d_url+setID)
        open(f"maps/{setID}.osz", "wb").write(response2.content)
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

download(["3968104"])
