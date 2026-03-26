import torch
import time
import numpy as np

from models.lstm_model import ContextLSTM
from telemetry.collector import collect_telemetry
from telemetry.preprocess import preprocess
from telemetry.logger import log_telemetry  # NEW IMPORT
from crypto_manager import lock_folder, red_tier_unlock, is_folder_unlocked
from ui_display import show_status
from wallpaper_manager import update_wallpaper

INPUT_SIZE = 11
HIDDEN_SIZE = 32
NUM_CLASSES = 3
SEQUENCE_LENGTH = 10

TRUSTED_NETWORKS = [
    "VITC-HOS2-4",
    "Raj's S25"
]

# warmup cycles to stabilize predictions
WARMUP_CYCLES = 5
warmup_counter = 0

model = ContextLSTM(INPUT_SIZE, HIDDEN_SIZE, NUM_CLASSES)
model.load_state_dict(torch.load("context_model.pth"))
model.eval()

sequence_buffer = []
app_history = []
current_tier = None

# ensure system starts visually in Green state
update_wallpaper("Green")


def normalize_app(app_name):

    if app_name in ["steam.exe", "steamwebhelper.exe"]:
        return "gaming"

    elif app_name == "Code.exe":
        return "dev"

    elif app_name == "chrome.exe":
        return "browse"

    else:
        return "idle"


def resolve_mode(app_history):

    counts = {"dev": 0, "browse": 0, "gaming": 0}

    for app in app_history:

        normalized = normalize_app(app)

        if normalized in counts:
            counts[normalized] += 1

    if counts["gaming"] > counts["dev"] and counts["gaming"] > counts["browse"]:
        return "Gaming"

    recent = app_history[-5:]

    if any(normalize_app(app) == "dev" for app in recent):
        return "Dev"

    if counts["browse"] > 0:
        return "Browsing"

    return "Idle"


def calculate_anomaly_score(app_history):

    score = 0.0
    switches = 0

    for i in range(1, len(app_history)):

        if normalize_app(app_history[i]) != normalize_app(app_history[i - 1]):
            switches += 1

    # increased threshold so normal multitasking does not trigger anomaly
    if switches > 25:
        score += 0.15

    return score


def calculate_final_risk(base_risk, mode, network, hour, anomaly_score):

    risk = base_risk

    if network and network not in TRUSTED_NETWORKS:
        risk += 0.2

    if 0 <= hour <= 5:
        risk += 0.1

    if mode == "Gaming":
        risk += 0.1

    elif mode == "Dev":
        risk -= 0.15

    elif mode == "Idle":
        risk -= 0.10

    risk += anomaly_score

    if risk < 0.5:
        risk *= 0.95

    return max(0.0, min(1.0, risk))


def determine_tier(risk):

    if risk < 0.35:
        return "Green"

    elif risk < 0.5:
        return "Yellow"

    else:
        return "Red"


while True:

    data = collect_telemetry()

    log_telemetry(data)  # NEW LINE

    vector = preprocess(data)

    sequence_buffer.append(vector)
    app_history.append(data["active_app"])

    if len(sequence_buffer) > SEQUENCE_LENGTH:
        sequence_buffer.pop(0)

    if len(app_history) > SEQUENCE_LENGTH:
        app_history.pop(0)

    print("Collecting context:", len(sequence_buffer), "/", SEQUENCE_LENGTH)

    if len(sequence_buffer) == SEQUENCE_LENGTH:

        input_seq = torch.tensor(
            np.array(sequence_buffer),
            dtype=torch.float32
        ).unsqueeze(0)

        with torch.no_grad():
            _, risk_pred = model(input_seq)

        base_risk = risk_pred.item()

        mode = resolve_mode(app_history)

        anomaly_score = calculate_anomaly_score(app_history)

        final_risk = calculate_final_risk(
            base_risk,
            mode,
            data["network"],
            data["hour"],
            anomaly_score
        )

        tier = determine_tier(final_risk)

        # warmup phase prevents system starting in Red
        if warmup_counter < WARMUP_CYCLES:
            warmup_counter += 1
            tier = "Green"

        if tier != current_tier:

            current_tier = tier

            # change wallpaper only when tier changes
            update_wallpaper(tier)

            if tier == "Red" and is_folder_unlocked():
                lock_folder()

        if tier == "Red" and not is_folder_unlocked():
            red_tier_unlock()

        show_status(
            mode,
            final_risk,
            tier,
            not is_folder_unlocked()
        )

    time.sleep(2)