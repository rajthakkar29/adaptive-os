import psutil
import platform
import subprocess
import datetime

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

    elif system == "Darwin":
        try:
            result = subprocess.check_output(
                ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"],
                encoding="utf-8"
            )
            for line in result.split("\n"):
                if " SSID" in line:
                    return line.split(":")[1].strip()
        except:
            return "Unknown"

    return "Unknown"

def collect_telemetry():
    return {
        "cpu": get_cpu_usage(),
        "hour": get_current_hour(),
        "active_app": get_active_process(),
        "network": get_network_name()
    }

if __name__ == "__main__":
    print(collect_telemetry())