import requests
import glob


REST_URL = "http://192.168.0.100:8090/tasks/create/file"
SAMPLE_FILE = glob.glob('/home/cuckoo/mal_pj/PJ1_malware/samples/normal/*')

HEADERS = {"Authorization": "Bearer eJhjD_vJ53F9Gp6wRdJv2Q"}

for i in SAMPLE_FILE : 
    with open(i, "rb") as sample:
        files = {"file": (i, sample)}
        r = requests.post(REST_URL, headers=HEADERS, files=files, timeout=30)
        task_id = r.json()["task_id"]