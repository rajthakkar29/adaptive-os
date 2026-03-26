import numpy as np

APP_CATEGORIES = ["Code.exe","chrome.exe","steam.exe","steamwebhelper.exe","explorer.exe","Unknown"]
NETWORK_CATEGORIES = ["VITC-HOS2-4", "Raj's S25", "Unknown"]

def one_hot_encode(value, categories):
    vector = [0] * len(categories)
    if value in categories:
        index = categories.index(value)
    else:
        index = categories.index("Unknown")
    vector[index] = 1
    return vector

def normalize(value, max_value):
    return value / max_value

def preprocess(telemetry):
    cpu = normalize(telemetry["cpu"], 100)
    hour = normalize(telemetry["hour"], 23)

    app_encoded = one_hot_encode(telemetry["active_app"], APP_CATEGORIES)
    network_encoded = one_hot_encode(telemetry["network"], NETWORK_CATEGORIES)

    feature_vector = [cpu, hour] + app_encoded + network_encoded
    return np.array(feature_vector)