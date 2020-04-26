# Standard library imports
from time import sleep
import re
from subprocess import Popen, PIPE

# Third party imports
import mss
import numpy as np
import cv2


def get_geo_string(window_id):
    out, err = Popen(["xdotool", "getwindowgeometry", window_id], stdout=PIPE).communicate()
    return out.decode('utf-8')


def get_window_id():
    proc = Popen(["xdotool", "search", "ZSNES"], stdout=PIPE)
    out, err = proc.communicate()
    return out.decode('utf-8')[:-1]


def parse_geometry_string(geo_string):
    geo_string = geo_string.replace("\n", "")
    regex = r'^Window \d{1,10}  Position: (\d{1,4}),(\d{1,4}) \(screen: \d{1,4}\)  Geometry: (\d{1,4})x(\d{1,4})'
    # Example: 'Window 48234499  Position: 1024,567 (screen: 0)  Geometry: 512x448'
    groups = re.match(regex, geo_string).groups()
    return tuple(int(el) for el in groups)


def get_game_geometry():
    geo_string = get_geo_string(get_window_id())
    left, top, width, height = parse_geometry_string(geo_string)
    # - 30, because for some reason xdotool gives the incorrect Y coordinate (consistently)
    return left, top - 30, width, height


def window_to_foreground(window_id):
    Popen(["xdotool", "windowactivate", window_id], stdout=PIPE).communicate()
    sleep(0.05)


def capture_gamewindow():
    left, top, width, height = get_game_geometry()
    monitor = {"top": top, "left": left, "width": width, "height": height}
    # window_to_foreground(get_window_id())
    img = mss.mss().grab(monitor)
    rgba = np.array(img)
    rgb = cv2.cvtColor(rgba, cv2.COLOR_RGBA2RGB)
    return rgb
