import psutil
import platform
import subprocess
import datetime
import time

import keyboard
import mouse

# tracking variables
key_count = 0
mouse_clicks = 0
mouse_distance = 0

last_mouse_pos = mouse.get_position()


def on_key(event):
    global key_count
    key_count += 1


def on_click(event):
    global mouse_clicks
    if event.event_type == 'down':
        mouse_clicks += 1


def track_mouse():
    global mouse_distance, last_mouse_pos

    current_pos = mouse.get_position()

    dx = current_pos[0] - last_mouse_pos[0]
    dy = current_pos[1] - last_mouse_pos[1]

    distance = (dx**2 + dy**2) ** 0.5

    mouse_distance += distance
    last_mouse_pos = current_pos


# start listeners
keyboard.on_press(on_key)
mouse.hook(on_click)


def get_cpu_usage():
    return psutil.cpu_percent(interval=1)


def get_current_hour():
    return datetime.datetime.now().hour


def get_active_process():
    try:
        import win32gui
        import win32process

        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        return process.name()
    except:
        return "Unknown"


def get_network_name():
    system = platform.system()

    if system == "Windows":
        try:
            result = subprocess.check_output(
                ["netsh", "wlan", "show", "interfaces"],
                encoding="utf-8"
            )
            for line in result.split("\n"):
                if "SSID" in line and "BSSID" not in line:
                    return line.split(":")[1].strip()
        except:
            return "Unknown"

    return "Unknown"


def collect_behavior():

    global key_count, mouse_clicks, mouse_distance

    # track mouse movement continuously
    track_mouse()

    behavior = {
        "keystrokes": key_count,
        "mouse_clicks": mouse_clicks,
        "mouse_distance": mouse_distance
    }

    # reset after reading (per interval)
    key_count = 0
    mouse_clicks = 0
    mouse_distance = 0

    return behavior


def collect_telemetry():

    behavior = collect_behavior()

    return {
        "cpu": get_cpu_usage(),
        "hour": get_current_hour(),
        "active_app": get_active_process(),
        "network": get_network_name(),
        "keystrokes": behavior["keystrokes"],
        "mouse_clicks": behavior["mouse_clicks"],
        "mouse_distance": behavior["mouse_distance"]
    }


if __name__ == "__main__":
    while True:
        print(collect_telemetry())
        time.sleep(2)