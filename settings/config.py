import json
import os

try:
    f = open("config.json")
    data = json.load(f)
    f.close()
except:
    data = {
        "DISCORD_TOKEN": os.environ["DISCORD_TOKEN"],
        "WOWS_TOKEN": os.environ["WOWS_TOKEN"]
    }
