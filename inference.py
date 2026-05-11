import torch
import time
import numpy as np
import json

from models.lstm_model import ContextLSTM
from telemetry.collector import collect_telemetry
from telemetry.preprocess import preprocess
from wallpaper_manager import update_wallpaper
from crypto_manager import lock_folder, red_tier_unlock

# ---------------- LOAD CONFIG ----------------
with open("config.json") as f:
    CONFIG = json.load(f)

INPUT_SIZE = 14
SEQ = CONFIG["sequence_length"]

# ---------------- LOAD BASELINE ----------------
with open("data/baseline.json") as f:
    BASELINE = json.load(f)


def z_score(value, mean, std):

    std = max(std, 1.0)

    return (value - mean) / std


# ---------------- MODEL ----------------
model = ContextLSTM(INPUT_SIZE, 32, 3)

model.load_state_dict(torch.load("context_model.pth"))

model.eval()

buffer = []

prev_risk = 0.3

current_tier = None

is_locked = False

last_prompt_time = 0

PROMPT_INTERVAL = CONFIG["prompt_interval"]

unlock_hold_until = 0

HOLD_DURATION = 10

red_counter = 0

RED_THRESHOLD = CONFIG["red_threshold"]


# ---------------- BEHAVIOR-DEFINED MODE ----------------
def get_mode(data):

    typing = data["typing_speed"]

    clicks = data["click_rate"]

    # focused work
    if typing > 4 and clicks < 1:
        return "Focused"

    # highly interactive usage
    elif clicks > 4 and typing < 2:
        return "Interactive"

    # balanced usage
    elif typing > 1 and clicks > 1:
        return "Browsing"

    # inactive
    else:
        return "Idle"


# ---------------- ADAPTIVE BEHAVIOR ----------------
def adaptive_behavior(risk, data):

    t = data["typing_speed"]

    c = data["click_rate"]

    t_z = z_score(
        t,
        BASELINE["typing"]["mean"],
        BASELINE["typing"]["std"]
    )

    click_std = BASELINE["clicks"]["std"]

    if click_std < 0.01:

        c_z = 0

    else:

        c_z = z_score(
            c,
            BASELINE["clicks"]["mean"],
            click_std
        )

    anomaly = abs(t_z) * 0.9 + abs(c_z) * 0.5

    if anomaly > 3.5:

        risk += 0.4

    elif anomaly > 2.5:

        risk += 0.2

    elif anomaly > 1.5:

        risk += 0.1

    else:

        risk -= 0.15

    return max(0.0, min(1.0, risk))


# ---------------- MODE ADJUSTMENT ----------------
def mode_adjustment(risk, mode):

    if mode == "Focused":

        risk -= 0.08

    elif mode == "Browsing":

        risk += 0.03

    elif mode == "Interactive":

        risk += 0.08

    elif mode == "Idle":

        risk -= 0.03

    return risk


# ---------------- NETWORK ADJUSTMENT ----------------
def network_adjustment(risk, network):

    trusted = CONFIG["trusted_networks"]

    if network and network not in trusted:

        risk += 0.08

    else:

        risk -= 0.03

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

        inp = torch.tensor(
            np.array(buffer),
            dtype=torch.float32
        ).unsqueeze(0)

        with torch.no_grad():

            _, r = model(inp)

        risk = r.item()

        # adaptive behavior
        risk = adaptive_behavior(risk, data)

        # calm idle reduction
        if (
            data["typing_speed"] < 0.5 and
            data["click_rate"] < 0.5
        ):

            risk *= 0.7

        # mode
        mode = get_mode(data)

        risk = mode_adjustment(risk, mode)

        # network
        risk = network_adjustment(
            risk,
            data["network"]
        )

        risk = max(0.0, min(1.0, risk))

        # smoothing
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

        # ---------------- SECURITY ----------------
        if tier == "Red" and not is_locked:

            is_locked = True

            lock_folder()

        if is_locked:

            tier = "Red"

            if (
                time.time() - last_prompt_time
                > PROMPT_INTERVAL
            ):

                success = red_tier_unlock()

                last_prompt_time = time.time()

                if success:

                    is_locked = False

                    unlock_hold_until = (
                        time.time() + HOLD_DURATION
                    )

                    red_counter = 0

                else:

                    is_locked = True

        # ---------------- WALLPAPER ----------------
        if is_locked:

            if current_tier != "Red":

                current_tier = "Red"

                update_wallpaper("Red")

        else:

            if tier != current_tier:

                current_tier = tier

                update_wallpaper(tier)

        print(
            f"Risk: {final:.3f} | "
            f"Tier: {tier} | "
            f"Mode: {mode} | "
            f"Net: {data['network']} | "
            f"T:{data['typing_speed']:.2f} "
            f"C:{data['click_rate']:.2f}"
        )

    time.sleep(2)