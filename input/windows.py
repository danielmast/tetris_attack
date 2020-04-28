# Source to code and and references
# http://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game
# https://www.win.tue.nl/~aeb/linux/kbd/scancodes-1.html
# https://www.win.tue.nl/~aeb/linux/kbd/scancodes-10.html

# Standard library imports
import ctypes
import time

# Local application imports
from input.input import Input
from constants import PLAYER, ACTION_KEY_MAPPING_P1, ACTION_KEY_MAPPING_P2

KEY_HEX_MAPPING = {
    'w': 0x11,
    'a': 0x1E,
    's': 0x1F,
    'd': 0x20,
    'f': 0x21,
    'g': 0x22,
    'n': 0x31,
    'm': 0x32,
    'u': 0x16,
    'j': 0x24,
    'h': 0x23,
    'k': 0x25,
    'l': 0x26,
    'y': 0x15,
    'F1': 0x3B,
    'F2': 0x3C,
    'F3': 0x3D,
    'F4': 0x3E,
    'SPACE': 0x39

}
SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input_II(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


class WindowsInput(Input):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_key(player, action):
        if player == PLAYER.ONE:
            return ACTION_KEY_MAPPING_P1[action]
        elif player == PLAYER.TWO:
            return ACTION_KEY_MAPPING_P2[action]
        raise Exception('Unexpected player: {}'.format(player))

    @staticmethod
    def key_down(key_string):
        key_hex = KEY_HEX_MAPPING[key_string]
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(0, key_hex, 0x0008, 0, ctypes.pointer(extra))
        x = Input_II(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    @staticmethod
    def key_up(key_string):
        key_hex = KEY_HEX_MAPPING[key_string]
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(0, key_hex, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
        x = Input_II(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    @staticmethod
    def press_key(key):
        WindowsInput.key_down(key)
        time.sleep(0.1)
        WindowsInput.key_up(key)

    def do_action(self, player, action):
        key = WindowsInput.get_key(player, action)
        WindowsInput.press_key(key)
