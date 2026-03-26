import ctypes
import os

# paths to wallpapers
GREEN_WALLPAPER = "wallpapers/green.jpg"
YELLOW_WALLPAPER = "wallpapers/yellow.jpg"
RED_WALLPAPER = "wallpapers/red.jpg"


def set_wallpaper(path):

    path = os.path.abspath(path)

    ctypes.windll.user32.SystemParametersInfoW(
        20,
        0,
        path,
        3
    )


def update_wallpaper(tier):

    if tier == "Green":
        set_wallpaper(GREEN_WALLPAPER)

    elif tier == "Yellow":
        set_wallpaper(YELLOW_WALLPAPER)

    elif tier == "Red":
        set_wallpaper(RED_WALLPAPER)