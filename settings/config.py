import json
import os
from utils.functions import get_base_path

try:
    config_path = os.path.join(get_base_path(), "config.json")
    f = open(config_path, encoding="utf-8")
    data = json.load(f)
    f.close()
except (FileNotFoundError, PermissionError, IsADirectoryError, json.JSONDecodeError, TypeError, OSError):
    data = {
        "DISCORD_TOKEN": os.environ["DISCORD_TOKEN"],
        "WOWS_TOKEN": os.environ["WOWS_TOKEN"]
    }
