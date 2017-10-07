import requests
import json

def save_map(name, map):
    requests.post("http://sploitbox.com/map.php", data={"name": name, "map": json.dumps(map)}).text

def get_map(name):
    return requests.post("http://sploitbox.com/map.php", data={"name": name}).text
