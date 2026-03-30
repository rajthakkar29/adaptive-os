import torch
import time
import numpy as np

from models.lstm_model import ContextLSTM
from telemetry.collector import collect_telemetry
from telemetry.preprocess import preprocess
from wallpaper_manager import update_wallpaper
from crypto_manager import lock_folder, red_tier_unlock

INPUT_SIZE = 14
SEQ = 10

TRUSTED_NETWORKS = ["VITC-HOS2-4", "Raj's S25"]

model = ContextLSTM(INPUT_SIZE, 32, 3)
model.load_state_dict(torch.load("context_model.pth"))
model.eval()

buffer = []
prev_risk = 0.3
current_tier = None

# 🔐 SECURITY STATE
is_locked = False
last_prompt_time = 0
PROMPT_INTERVAL = 10

unlock_hold_until = 0
HOLD_DURATION = 8


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

    if typing < 0.5 and clicks < 0.5:
        risk -= 0.15

    elif typing < 2 and clicks < 2:
        risk -= 0.05

    elif typing > 8 or clicks > 10:
        risk += 0.35

    elif typing > 5 or clicks > 6:
        risk += 0.2

    return risk


# ---------------- MODE ----------------
def mode_adjustment(risk, mode):

    if mode == "Dev":
        risk -= 0.15
    elif mode == "Browsing":
        risk += 0.05
    elif mode == "Gaming":
        risk += 0.12
    elif mode == "Idle":
        risk -= 0.10

    return risk


# ---------------- NETWORK ----------------
def network_adjustment(risk, network):

    if network and network not in TRUSTED_NETWORKS:
        risk += 0.15
    else:
        risk -= 0.05

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

        # pipeline
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

        final = 0.5 * prev_risk + 0.5 * risk
        prev_risk = final

        # ---------------- TIER ----------------
        if time.time() < unlock_hold_until:
            tier = "Yellow"
        else:
            if final < 0.35:
                tier = "Green"
            elif final < 0.5:
                tier = "Yellow"
            else:
                tier = "Red"

        # ---------------- SECURITY (STATE BASED) ----------------
        if tier == "Red" and not is_locked:
            is_locked = True
            lock_folder()

        if is_locked:

            tier = "Red"  # force

            if time.time() - last_prompt_time > PROMPT_INTERVAL:

                success = red_tier_unlock()
                last_prompt_time = time.time()

                if success:
                    is_locked = False
                    unlock_hold_until = time.time() + HOLD_DURATION

        # ---------------- WALLPAPER ----------------
        if tier != current_tier:
            current_tier = tier
            update_wallpaper(tier)

        print(
            f"Risk: {final:.3f} | Tier: {tier} | "
            f"Mode: {mode} | Net: {data['network']} | "
            f"T:{data['typing_speed']:.2f} C:{data['click_rate']:.2f}"
        )

    time.sleep(2)