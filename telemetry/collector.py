import psutil
import platform
import subprocess
import datetime
import time
from pynput import keyboard, mouse

# global counters
key_count = 0
click_count = 0
last_time = time.time()


def on_press(key):
    global key_count
    key_count += 1


def on_click(x, y, button, pressed):
    global click_count
    if pressed:
        click_count += 1


# start listeners (runs in background)
keyboard_listener = keyboard.Listener(on_press=on_press)
mouse_listener = mouse.Listener(on_click=on_click)

keyboard_listener.start()
mouse_listener.start()


def get_cpu_usage():
    return psutil.cpu_percent(interval=0.5)


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


def get_behavior_metrics():
    global key_count, click_count, last_time

    current_time = time.time()
    duration = current_time - last_time

    if duration == 0:
        duration = 1

    typing_speed = key_count / duration
    click_rate = click_count / duration

    # reset counters after calculation
    key_count = 0
    click_count = 0
    last_time = current_time

    return typing_speed, click_rate


def collect_telemetry():
    typing_speed, click_rate = get_behavior_metrics()

    return {
        "cpu": get_cpu_usage(),
        "hour": get_current_hour(),
        "active_app": get_active_process(),
        "network": get_network_name(),
        "typing_speed": typing_speed,
        "click_rate": click_rate
    }


if __name__ == "__main__":
    while True:
        print(collect_telemetry())
        time.sleep(2)