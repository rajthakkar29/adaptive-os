import torch
import time
import numpy as np

from models.lstm_model import ContextLSTM
from telemetry.collector import collect_telemetry
from telemetry.preprocess import preprocess
from wallpaper_manager import update_wallpaper
from crypto_manager import lock_folder, red_tier_unlock

INPUT_SIZE = 14
SEQ = 20

TRUSTED_NETWORKS = ["VITC-HOS2-4", "Raj's S25"]

model = ContextLSTM(INPUT_SIZE, 32, 3)
model.load_state_dict(torch.load("context_model.pth"))
model.eval()

buffer = []
prev_risk = 0.3
current_tier = None

# SECURITY STATE
is_locked = False
last_prompt_time = 0
PROMPT_INTERVAL = 15

unlock_hold_until = 0
HOLD_DURATION = 10

#  stability control
red_counter = 0
RED_THRESHOLD = 3


# ---------------- MODE ----------------
def get_mode(app):
    if app == "Code.exe":
        return "Dev"
    elif app == "chrome.exe":
        return "Browsing"
    elif app in ["steam.exe", "steamwebhelper.exe"]:
        return "Gaming"
    else:
        return "Idle"


# ---------------- BEHAVIOR ----------------
def behavior_adjustment(risk, typing, clicks):

    #  suspicious very low irregular typing
    if 0 < typing < 0.3 and clicks < 0.2:
        risk += 0.10

    #  idle
    elif typing < 0.5 and clicks < 0.5:
        risk -= 0.05

    #  normal
    elif typing < 3 and clicks < 2:
        pass

    #  abnormal
    elif typing > 5 or clicks > 6:
        risk += 0.25

    #  extreme
    if typing > 12 or clicks > 10:
        risk += 0.35

    return risk


# ---------------- MODE ----------------
def mode_adjustment(risk, mode):

    if mode == "Dev":
        risk -= 0.12
    elif mode == "Browsing":
        risk += 0.05
    elif mode == "Gaming":
        risk += 0.10
    elif mode == "Idle":
        risk -= 0.04

    return risk


# ---------------- NETWORK ----------------
def network_adjustment(risk, network):

    if network and network not in TRUSTED_NETWORKS:
        risk += 0.12
    else:
        risk -= 0.02

    return risk


# ---------------- INIT ----------------
update_wallpaper("Green")


while True:

    data = collect_telemetry()
    vec = preprocess(data)

    buffer.append(vec)

    if len(buffer) > SEQ:
        buffer.pop(0)

    if len(buffer) == SEQ:

        inp = torch.tensor(np.array(buffer), dtype=torch.float32).unsqueeze(0)

        with torch.no_grad():
            _, r = model(inp)

        base_risk = r.item()

        # ---------------- PIPELINE ----------------
        risk = base_risk

        risk = behavior_adjustment(
            risk,
            data["typing_speed"],
            data["click_rate"]
        )

        mode = get_mode(data["active_app"])
        risk = mode_adjustment(risk, mode)

        risk = network_adjustment(risk, data["network"])

        risk = max(0.0, min(1.0, risk))

        #  smoother but responsive
        final = 0.4 * prev_risk + 0.6 * risk
        prev_risk = final

        # ---------------- TIER ----------------
        if final > 0.5:
            red_counter += 1
        else:
            red_counter = 0

        if time.time() < unlock_hold_until:
            tier = "Yellow"

        elif red_counter >= RED_THRESHOLD:
            tier = "Red"

        elif final < 0.35:
            tier = "Green"

        else:
            tier = "Yellow"

        # ---------------- WALLPAPER FIRST ----------------
        if tier != current_tier:
            current_tier = tier
            update_wallpaper(tier)

        # ---------------- SECURITY ----------------
        if tier == "Red" and not is_locked:
            is_locked = True
            lock_folder()

        if is_locked:

            tier = "Red"

            if time.time() - last_prompt_time > PROMPT_INTERVAL:

                success = red_tier_unlock()
                last_prompt_time = time.time()

                if success:
                    is_locked = False
                    unlock_hold_until = time.time() + HOLD_DURATION
                    red_counter = 0

        print(
            f"Risk: {final:.3f} | Tier: {tier} | "
            f"Mode: {mode} | Net: {data['network']} | "
            f"T:{data['typing_speed']:.2f} C:{data['click_rate']:.2f}"
        )

    time.sleep(2)