# Standard library imports
import time
import math
import subprocess

# Third party imports
import cv2
import numpy as np
import win32gui

# Local application imports
import laurens
import gamekeyboard
import grabscreen

# Amounts
PLAYFIELD_ROW_AMOUNT = 12
PLAYFIELD_COLUMN_AMOUNT = 6
PANEL_TYPE_AMOUNT = 7
GARBAGE_TYPE_AMOUNT = 2
TILE_TYPE_AMOUNT = PANEL_TYPE_AMOUNT + GARBAGE_TYPE_AMOUNT
CURSOR_ROW_LIMIT = PLAYFIELD_ROW_AMOUNT - 1
CURSOR_COLUMN_LIMIT = PLAYFIELD_COLUMN_AMOUNT - 2

# Pixel dimensions
TILE_SIZE = 16
PLAYFIELD_WIDTH = TILE_SIZE * PLAYFIELD_COLUMN_AMOUNT
PLAYFIELD_HEIGHT = TILE_SIZE * PLAYFIELD_ROW_AMOUNT
CURSOR_WIDTH = 35
CURSOR_HEIGHT = 20

# Emulator Settings
WINDOW_NAME = "Tetris Attack (U) [!] - Snes9x 1.60"
EMULATOR_PATH = "D:/Development/Python/tetris-attack/emulator/snes9x/snes9x-x64.exe"
ROM_PATH = "Tetris Attack (U) [!].smc"

# Actions
MOVE_UP = 1
MOVE_DOWN = 2
MOVE_LEFT = 3
MOVE_RIGHT = 4
SWITCH_PANELS = 5
STACK_UP = 6
DO_NOTHING = 7

# Other
LEFT = -1
RIGHT = 1

# Tile types
TILES = {
    'PURPLE': 0,
    'YELLOW': 1,
    'GREEN': 2,
    'AQUAMARINE': 3,
    'RED': 4,
    'GREY': 5,
    'BLUE': 6,
    'CONCRETE': 7,
    'STEEL': 8
}

# Keyboard keys
ACTION_KEY_MAPPING = {
    MOVE_UP: 'W',
    MOVE_DOWN: 'S',
    MOVE_LEFT: 'A',
    MOVE_RIGHT: 'D',
    SWITCH_PANELS: 'F',
    STACK_UP: 'M'
}


def list_to_string(list):
    return " ".join(map(str, list))

# Color to tile mapping
COLOR_TILE_MAPPING = {
    list_to_string([255,  24, 255]): TILES['PURPLE'],
    list_to_string([255, 255,   0]): TILES['YELLOW'],
    list_to_string([  0, 255,   0]): TILES['GREEN'],
    list_to_string([  0, 255, 255]): TILES['AQUAMARINE'],
    list_to_string([255,  16,  16]): TILES['RED'],
    list_to_string([132, 134, 132]): TILES['GREY'],
    list_to_string([ 66, 113, 255]): TILES['BLUE'],
    list_to_string([  8,  81, 214]): TILES['CONCRETE'],
    list_to_string([148,  24,  24]): TILES['CONCRETE'],
    list_to_string([ 99, 105, 107]): TILES['STEEL'],
    list_to_string([ 57,  56,  57]): TILES['STEEL']
}


def press_key(key_string):
    gamekeyboard.PressKey(key_string)
    time.sleep(0.1)
    gamekeyboard.ReleaseKey(key_string)


def start_game(start_emulator=True, wait_time=2, load_game_type=None):
    if start_emulator:
        subprocess.Popen([EMULATOR_PATH, ROM_PATH])

    time.sleep(wait_time)

    if load_game_type == "vs":
        press_key("F1")
    elif load_game_type == "single_player":
        press_key("F2")


def perform_countdown(seconds):
    while seconds > 0:
        print("%d..." % seconds)
        time.sleep(1)
        seconds -= 1


def get_screenshot(coords=None):
    return grabscreen.grab_screen(region=coords)


def determine_playfield_coords():
    offset_x = 16
    offset_y = 93

    window = win32gui.FindWindow(None, WINDOW_NAME)
    window_coords = win32gui.GetWindowRect(window)

    game_start_x = window_coords[0] + offset_x
    game_start_y = window_coords[1] + offset_y
    game_end_x = game_start_x + PLAYFIELD_WIDTH
    game_end_y = game_start_y + PLAYFIELD_HEIGHT

    return [game_start_x, game_start_y, game_end_x, game_end_y]


def determine_cursor_coords(screenshot):
    offset_x = -12
    offset_y = 1

    template = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [255, 255, 255, 255, 0, 255, 255, 255, 255, 255],
        [255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
        [0, 0, 0, 255, 255, 255, 255, 0, 0, 0],
    ], dtype=np.uint8)
    screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    result = cv2.matchTemplate(screenshot_gray, template, method=cv2.TM_CCOEFF)
    min_value, max_value, min_coords, max_coords = cv2.minMaxLoc(result)

    cursor_start_x = max_coords[0] + offset_x
    cursor_start_y = max_coords[1] + offset_y
    cursor_end_x = cursor_start_x + CURSOR_WIDTH
    cursor_end_y = cursor_start_y + CURSOR_HEIGHT

    return [cursor_start_x, cursor_start_y, cursor_end_x, cursor_end_y]


def determine_cursor_position(cursor_coords):
    offset_row = 0
    offset_column = 0

    cursor_row = math.floor((cursor_coords[1] + (TILE_SIZE / 2)) / TILE_SIZE) + offset_row
    cursor_column = math.floor((cursor_coords[0] + (TILE_SIZE / 2)) / TILE_SIZE) + offset_column

    return cursor_row, cursor_column


def determine_tile_type(pixel):
    color_string = list_to_string(list(pixel))

    if color_string in COLOR_TILE_MAPPING:
        return COLOR_TILE_MAPPING[color_string]
    else:
        return None


def determine_playfield_matrices(screenshot, cursor_coords):
    playfield_matrices = np.zeros((PLAYFIELD_ROW_AMOUNT, PLAYFIELD_COLUMN_AMOUNT, TILE_TYPE_AMOUNT))

    start_x = round(TILE_SIZE / 2)
    start_y = (cursor_coords[1] + round(CURSOR_HEIGHT / 2)) % TILE_SIZE

    # Loop over all blocks
    current_row = 0
    current_column = 0
    while current_row < PLAYFIELD_ROW_AMOUNT:
        while current_column < PLAYFIELD_COLUMN_AMOUNT:
            tile_x = int(start_x + (current_column * TILE_SIZE))
            tile_y = int(start_y + (current_row * TILE_SIZE))
            tile_type = determine_tile_type(screenshot[tile_y, tile_x])
            if tile_type is not None:
                playfield_matrices[current_row, current_column, tile_type] = 1
            current_column += 1
        current_row += 1
        current_column = 0

    return playfield_matrices


def main():
    start_game(start_emulator=True, wait_time=2, load_game_type="single_player")
    playfield_coords = determine_playfield_coords()
    bot = laurens.Laurens(TILES)

    while True:
        playfield_screenshot = get_screenshot(playfield_coords)
        cursor_coords = determine_cursor_coords(playfield_screenshot)
        cursor_position = determine_cursor_position(cursor_coords)
        playfield_matrices = determine_playfield_matrices(playfield_screenshot, cursor_coords)
        action = bot.get_action(playfield_matrices, cursor_position)
        press_key(ACTION_KEY_MAPPING[action])


main()