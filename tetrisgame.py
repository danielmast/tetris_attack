import time
from PIL import ImageGrab
import cv2
import numpy as np
import win32gui
import math
import subprocess

import tetrisplayer
import gamekeyboard

# Panel colors
PURPLE =            [255,  24, 255]
YELLOW =            [255, 255,   0]
GREEN =             [  0, 255,   0]
AQUAMARINE =        [  0, 255, 255]
RED =               [255,  16,  16]
GREY =              [132, 134, 132]
BLUE =              [ 66, 113, 255]

# Garbage colors
GARBAGE_BLUE =      [  8,  81, 214]
GARBAGE_RED =       [148,  24,  24]
GARBAGE_LIGHTGREY = [ 99, 105, 107]
GARBAGE_DARKGREY =  [ 57,  56,  57]

# Tile types
PANEL_PURPLE = 0
PANEL_YELLOW = 1
PANEL_GREEN = 2
PANEL_AQUAMARINE = 3
PANEL_RED = 4
PANEL_GREY = 5
PANEL_BLUE = 6
GARBAGE_CONCRETE = 7
GARBAGE_STEEL = 8

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

# Actions
MOVE_UP = 1
MOVE_DOWN = 2
MOVE_LEFT = 3
MOVE_RIGHT = 4
SWITCH_PANELS = 5
STACK_UP = 6
DO_NOTHING = 7

# Keyboard keys
KEYS = {
    MOVE_UP: 'W',
    MOVE_DOWN: 'S',
    MOVE_LEFT: 'A',
    MOVE_RIGHT: 'D',
    SWITCH_PANELS: 'F',
    STACK_UP: 'M'
}

# Directions
LEFT = -1
RIGHT = 1

# Emulator
WINDOW_NAME = "Tetris Attack (U) [!] - Snes9x 1.60"
EMULATOR_PATH = "D:/Development/Python/tetris-attack/emulator/snes9x/snes9x-x64.exe"
ROM_PATH = "Tetris Attack (U) [!].smc"


def press_key(key_string):
    key = gamekeyboard.KEYS[key_string]
    gamekeyboard.PressKey(key)
    time.sleep(0.1)
    gamekeyboard.ReleaseKey(key)


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


def take_screenshot(coords=None):
    return ImageGrab.grab(bbox=coords)


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


def determine_cursor_coords(screenshot_pil):
    offset_x = -12
    offset_y = 1

    template = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [255, 255, 255, 255, 0, 255, 255, 255, 255, 255],
        [255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
        [0, 0, 0, 255, 255, 255, 255, 0, 0, 0],
    ], dtype=np.uint8)
    screenshot_cv2 = cv2.cvtColor(np.array(screenshot_pil), cv2.COLOR_RGB2GRAY)

    result = cv2.matchTemplate(screenshot_cv2, template, method=cv2.TM_CCOEFF)
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
    color = list(pixel)

    if color == PURPLE:
        return PANEL_PURPLE
    elif color == YELLOW:
        return PANEL_YELLOW
    elif color == GREEN:
        return PANEL_GREEN
    elif color == AQUAMARINE:
        return PANEL_AQUAMARINE
    elif color == RED:
        return PANEL_RED
    elif color == GREY:
        return PANEL_GREY
    elif color == BLUE:
        return PANEL_BLUE
    elif color == GARBAGE_BLUE or color == GARBAGE_RED:
        return GARBAGE_CONCRETE
    elif color == GARBAGE_LIGHTGREY or color == GARBAGE_DARKGREY:
        return GARBAGE_STEEL
    else:
        return None


def determine_playfield_matrices(screenshot_pil, cursor_coords):
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
            tile_type = determine_tile_type(screenshot_pil.getpixel((tile_x, tile_y)))
            if tile_type is not None:
                playfield_matrices[current_row, current_column, tile_type] = 1
            current_column += 1
        current_row += 1
        current_column = 0

    return playfield_matrices


def main():
    start_game(start_emulator=True, wait_time=2, load_game_type="single_player")
    playfield_coords = determine_playfield_coords()
    tp = tetrisplayer.TetrisPlayer()

    while True:
        playfield_screenshot = take_screenshot(playfield_coords)
        cursor_coords = determine_cursor_coords(playfield_screenshot)
        cursor_position = determine_cursor_position(cursor_coords)
        playfield_matrices = determine_playfield_matrices(playfield_screenshot, cursor_coords)
        action = tp.determine_next_action(playfields_matrices, cursor_position)
        press_key(KEYS[action])


main()