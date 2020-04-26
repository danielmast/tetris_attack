# Standard library imports
from time import sleep
import re
from subprocess import Popen, PIPE

# Third party imports
import mss
import numpy as np
import cv2

# Local application imports
from screencapturer.screencapturer import ScreenCapturer


# Constant colors
CONCRETE_BLUE = [8, 81, 214]
PURPLE = [255, 24, 255]
YELLOW = [255, 255, 0]
GREEN = [0, 255, 0]
AQUAMARINE = [0, 255, 255]
RED = [255, 16, 16]
WHITE = [248, 248, 248]

# Constant blocks
BLOCK_ROW_AMOUNT = 12
BLOCK_COLUMN_AMOUNT = 6

BLOCK_PURPLE = 10
BLOCK_YELLOW = 11
BLOCK_GREEN = 12
BLOCK_AQUAMARINE = 13
BLOCK_RED = 14

# Constant pixel sizes
BLOCK_SIZE = 16
GAME_WIDTH = BLOCK_SIZE * BLOCK_COLUMN_AMOUNT
GAME_HEIGHT = BLOCK_SIZE * BLOCK_ROW_AMOUNT
PLAYER_WIDTH = 35
PLAYER_HEIGHT = 20


class LinuxScreenCapturer(ScreenCapturer):

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_geo_string(window_id):
        out, err = Popen(["xdotool", "getwindowgeometry", window_id], stdout=PIPE).communicate()
        return out.decode('utf-8')

    @staticmethod
    def get_window_id():
        proc = Popen(["xdotool", "search", "ZSNES"], stdout=PIPE)
        out, err = proc.communicate()
        return out.decode('utf-8')[:-1]

    @staticmethod
    def parse_geometry_string(geo_string):
        geo_string = geo_string.replace("\n", "")
        regex = r'^Window \d{1,10}  Position: (\d{1,4}),(\d{1,4}) \(screen: \d{1,4}\)  Geometry: (\d{1,4})x(\d{1,4})'
        # Example: 'Window 48234499  Position: 1024,567 (screen: 0)  Geometry: 512x448'
        groups = re.match(regex, geo_string).groups()
        return tuple(int(el) for el in groups)

    @staticmethod
    def get_game_geometry():
        geo_string = LinuxScreenCapturer.get_geo_string(LinuxScreenCapturer.get_window_id())
        left, top, width, height = LinuxScreenCapturer.parse_geometry_string(geo_string)
        # - 30, because for some reason xdotool gives the incorrect Y coordinate (consistently)
        return left, top - 30, width, height

    @staticmethod
    def window_to_foreground(window_id):
        Popen(["xdotool", "windowactivate", window_id], stdout=PIPE).communicate()
        sleep(0.05)

    def capture_playfield(self, ):
        left, top, width, height = LinuxScreenCapturer.get_game_geometry()
        monitor = {"top": top, "left": left, "width": width, "height": height}
        # window_to_foreground(get_window_id())
        img = mss.mss().grab(monitor)
        rgba = np.array(img)
        rgb = cv2.cvtColor(rgba, cv2.COLOR_RGBA2RGB)
        return rgb
