import json
import os

LOG_FILE = "telemetry_logs.json"


def log_data(data):

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except:
        logs = []

    logs.append(data)

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)