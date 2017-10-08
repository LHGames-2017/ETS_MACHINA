import requests
import json

# Save the map to my server in JSON format
def save_map(name, map):
    requests.post("http://sploitbox.com/map.php", data={"name": name, "map": json.dumps(map)}).text

# Get the map from my server in JSON format
def get_map(name):
    return requests.post("http://sploitbox.com/map.php", data={"name": name}).text
