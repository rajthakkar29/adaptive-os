import numpy as np

APP_CATEGORIES = [
    "Code.exe",
    "chrome.exe",
    "steam.exe",
    "steamwebhelper.exe",
    "explorer.exe",
    "Notepad.exe",
    "Unknown"
]

NETWORK_CATEGORIES = [
    "VITC-HOS2-4",
    "Raj's S25",
    "Unknown"
]


def one_hot_encode(value, categories):
    vector = [0] * len(categories)

    if value in categories:
        index = categories.index(value)
    else:
        index = categories.index("Unknown")

    vector[index] = 1
    return vector


def normalize(value, max_value):
    return min(value / max_value, 1.0)


def preprocess(data):
    cpu = normalize(data["cpu"], 100)
    hour = normalize(data["hour"], 23)

    typing = normalize(data.get("typing_speed", 0), 10)
    clicks = normalize(data.get("click_rate", 0), 10)

    app = one_hot_encode(data["active_app"], APP_CATEGORIES)
    network = one_hot_encode(data["network"], NETWORK_CATEGORIES)

    return np.array([cpu, hour, typing, clicks] + app + network)