# Standard library imports
import math
from types import SimpleNamespace
import time

# Third party imports
import cv2
import numpy as np
import win32gui

# Local application imports
import grabscreen

cursor_position = []
playfield_matrices = []

AMOUNT = SimpleNamespace(**{
    'PLAYFIELD_ROWS': 12,
    'PLAYFIELD_COLUMNS': 6,
    'TILE_TYPES': 9,
    'CURSOR_ROWS': 11,
    'CURSOR_COLUMNS': 4
})

PIXELSIZE = SimpleNamespace(**{
    'TILE_WIDTH': 16,
    'TILE_HEIGHT': 16,
    'PLAYFIELD_WIDTH': 16 * 6,
    'PLAYFIELD_HEIGHT': 16 * 12,
    'CURSOR_WIDTH': 35,
    'CURSOR_HEIGHT': 20
})

DIRECTION = SimpleNamespace(**{
    'LEFT': -1,
    'RIGHT': 1
})

ACTION = SimpleNamespace(**{
    'MOVE_UP' : 1,
    'MOVE_DOWN' : 2,
    'MOVE_LEFT' : 3,
    'MOVE_RIGHT' : 4,
    'SWITCH_PANELS' : 5,
    'STACK_UP' : 6,
    'DO_NOTHING' : 7
})
MOVES = [ACTION.MOVE_UP, ACTION.MOVE_DOWN, ACTION.MOVE_LEFT, ACTION.MOVE_RIGHT]

TILE = SimpleNamespace(**{
    'PURPLE': 0,
    'YELLOW': 1,
    'GREEN': 2,
    'AQUAMARINE': 3,
    'RED': 4,
    'GREY': 5,
    'BLUE': 6,
    'CONCRETE': 7,
    'STEEL': 8
})
PANELS = [TILE.PURPLE, TILE.YELLOW, TILE.GREEN, TILE.AQUAMARINE, TILE.RED, TILE.GREY, TILE.BLUE]
GARBAGE = [TILE.CONCRETE, TILE.STEEL]

ACTION_KEY_MAPPING = {
    ACTION.MOVE_UP: 'W',
    ACTION.MOVE_DOWN: 'S',
    ACTION.MOVE_LEFT: 'A',
    ACTION.MOVE_RIGHT: 'D',
    ACTION.SWITCH_PANELS: 'F',
    ACTION.STACK_UP: 'M'
}

COLOR_TILE_MAPPING = {
    " ".join(map(str, [255,  24, 255])): TILE.PURPLE,
    " ".join(map(str, [255, 255,   0])): TILE.YELLOW,
    " ".join(map(str, [  0, 255,   0])): TILE.GREEN,
    " ".join(map(str, [  0, 255, 255])): TILE.AQUAMARINE,
    " ".join(map(str, [255,  16,  16])): TILE.RED,
    " ".join(map(str, [132, 134, 132])): TILE.GREY,
    " ".join(map(str, [ 66, 113, 255])): TILE.BLUE,
    " ".join(map(str, [  8,  81, 214])): TILE.CONCRETE,
    " ".join(map(str, [148,  24,  24])): TILE.CONCRETE,
    " ".join(map(str, [ 99, 105, 107])): TILE.STEEL,
    " ".join(map(str, [ 57,  56,  57])): TILE.STEEL
}


def get_screenshot(coords=None):
    return grabscreen.grab_screen(region=coords)


def determine_playfield_coords():
    WINDOW_NAME = "Tetris Attack (U) [!] - Snes9x 1.60"
    offset_x = 16
    offset_y = 93

    window = win32gui.FindWindow(None, WINDOW_NAME)
    window_coords = win32gui.GetWindowRect(window)

    game_start_x = window_coords[0] + offset_x
    game_start_y = window_coords[1] + offset_y
    game_end_x = game_start_x + PIXELSIZE.PLAYFIELD_WIDTH
    game_end_y = game_start_y + PIXELSIZE.PLAYFIELD_HEIGHT

    return [game_start_x, game_start_y, game_end_x, game_end_y]


def determine_cursor_coords(screenshot):
    offset_x = -12
    offset_y = 1

    #template = np.array([
    #    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #    [255, 255, 255, 255, 0, 255, 255, 255, 255, 255],
    #    [255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    #    [0, 0, 0, 255, 255, 255, 255, 0, 0, 0],
    #], dtype=np.uint8)
    template = np.load('npy/cursor_center.npy')
    screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    result = cv2.matchTemplate(screenshot_gray, template, method=cv2.TM_CCOEFF)
    min_value, max_value, min_coords, max_coords = cv2.minMaxLoc(result)

    cursor_start_x = max_coords[0] + offset_x
    cursor_start_y = max_coords[1] + offset_y
    cursor_end_x = cursor_start_x + PIXELSIZE.CURSOR_WIDTH
    cursor_end_y = cursor_start_y + PIXELSIZE.CURSOR_HEIGHT

    return [cursor_start_x, cursor_start_y, cursor_end_x, cursor_end_y]


def determine_cursor_position(cursor_coords):
    offset_row = 0
    offset_column = 0

    cursor_row = math.floor((cursor_coords[1] + (PIXELSIZE.TILE_HEIGHT / 2)) / PIXELSIZE.TILE_HEIGHT) + offset_row
    cursor_column = math.floor((cursor_coords[0] + (PIXELSIZE.TILE_WIDTH / 2)) / PIXELSIZE.TILE_WIDTH) + offset_column

    return cursor_row, cursor_column


def determine_tile_type(pixel):
    color_string = " ".join(map(str, (list(pixel))))

    if color_string in COLOR_TILE_MAPPING:
        return COLOR_TILE_MAPPING[color_string]
    else:
        return None


def determine_playfield_matrices(screenshot, cursor_coords):
    playfield_matrices = np.zeros((AMOUNT.PLAYFIELD_ROWS, AMOUNT.PLAYFIELD_COLUMNS, AMOUNT.TILE_TYPES))

    start_x = round(PIXELSIZE.TILE_WIDTH / 2)
    start_y = (cursor_coords[1] + round(PIXELSIZE.CURSOR_HEIGHT / 2)) % PIXELSIZE.TILE_HEIGHT

    # Loop over all blocks
    current_row = 0
    current_column = 0
    while current_row < AMOUNT.PLAYFIELD_ROWS:
        while current_column < AMOUNT.PLAYFIELD_COLUMNS:
            tile_x = int(start_x + (current_column * PIXELSIZE.TILE_WIDTH))
            tile_y = int(start_y + (current_row * PIXELSIZE.TILE_HEIGHT))
            tile_type = determine_tile_type(screenshot[tile_y, tile_x])
            if tile_type is not None:
                playfield_matrices[current_row, current_column, tile_type] = 1
            current_column += 1
        current_row += 1
        current_column = 0

    return playfield_matrices


def start():
    playfield_coords = determine_playfield_coords()
    last_time = 0
    while True:
        playfield_screenshot = get_screenshot(playfield_coords)
        cursor_coords = determine_cursor_coords(playfield_screenshot)
        cursor_position = determine_cursor_position(cursor_coords)
        playfield_matrices = determine_playfield_matrices(playfield_screenshot, cursor_coords)
        current_time = time.time()
        fps = 1 / (current_time - last_time)
        print(time.sec, fps)
        last_time = current_time


start()