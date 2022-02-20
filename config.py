import json
import os

try:
    f = open("config.json")
    data = json.load(f)
    f.close()
except:
    data = {
        "PREFIX": os.environ["PREFIX"],
        "TOKEN": os.environ["TOKEN"],
        "APPLICATION_ID": os.environ["APPLICATION_ID"]
    }
