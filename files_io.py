import json
import time

def write_json_array(json_obj : str, path : str):
    with open(path, 'w') as file:
        json.dump(json_obj, file, ensure_ascii = False)

def timestamp():
    with open('temp_data/last_request_time', 'w') as file:
        t = str(round(time.time()))
        file.write(t)
        