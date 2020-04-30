# Standard library imports
import math
import time
import platform
from multiprocessing import shared_memory

# Third party imports
import cv2
import numpy as np

# Local application imports
from constants import *
import gamestate
if platform.system().lower() == OS.WINDOWS:
    import screencapturer.windows as screencapturer
elif platform.system().lower() == OS.LINUX:
    import screencapturer.linux as screencapturer


class ImageProcessor():
    @staticmethod
    def extract_playfields_from_gamewindow(gamewindow):
        playfields = []

        if gamewindow.shape[1] > PIXELSIZE.GAMEWINDOW_WIDTH:
            gamewindow_offset_y = PIXELSIZE.GAMEWINDOW_OFFSET_Y
            gamewindow_offset_x = PIXELSIZE.GAMEWINDOW_OFFSET_X
        else:
            gamewindow_offset_y = 0
            gamewindow_offset_x = 0

        y1 = gamewindow_offset_y + PIXELSIZE.PLAYFIELD_OFFSET_Y
        y2 = y1 + PIXELSIZE.PLAYFIELD_HEIGHT
        x1_p1 = gamewindow_offset_x + PIXELSIZE.PLAYFIELD_OFFSET_X_P1
        x2_p1 = x1_p1 + PIXELSIZE.PLAYFIELD_WIDTH
        x1_p2 = gamewindow_offset_x + PIXELSIZE.PLAYFIELD_OFFSET_X_P2
        x2_p2 = x1_p2 + PIXELSIZE.PLAYFIELD_WIDTH

        playfields.append(gamewindow[y1:y2, x1_p1:x2_p1])
        playfields.append(gamewindow[y1:y2, x1_p2:x2_p2])

        return playfields

    @staticmethod
    def determine_cursor_coords(playfield):
        template = np.load('npy/cursor_center.npy')
        screenshot_gray = cv2.cvtColor(np.array(playfield), cv2.COLOR_RGB2GRAY)

        result = cv2.matchTemplate(screenshot_gray, template, method=cv2.TM_CCOEFF)
        min_value, max_value, min_coords, max_coords = cv2.minMaxLoc(result)

        if max_value > 600000:  # Threshold coefficient
            screenshot_determine_y = screenshot_gray[max_coords[1] + 2, max_coords[0] + 16]
            if screenshot_determine_y == 255:
                offset_y = 2
            else:
                offset_y = 3

            offset_x = -11

            cursor_x = max_coords[0] + offset_x
            cursor_y = max_coords[1] + offset_y

            return cursor_x, cursor_y

    @staticmethod
    def determine_cursor_position(cursor_coords):
        if cursor_coords is not None:
            cursor_row = math.floor((cursor_coords[1] + (PIXELSIZE.TILE_HEIGHT / 2)) / PIXELSIZE.TILE_HEIGHT)
            cursor_column = math.floor((cursor_coords[0] + (PIXELSIZE.TILE_WIDTH / 2)) / PIXELSIZE.TILE_WIDTH)

            return cursor_row, cursor_column

    @staticmethod
    def determine_tile_type(pixel):
        color_string = " ".join(map(str, (list(pixel))))

        if color_string in COLOR_TILE_MAPPING:
            return COLOR_TILE_MAPPING[color_string]
        elif np.any(pixel > 100):
            return TILE.UNKNOWN
        else:
            return None

    @staticmethod
    def determine_playfield_matrices(screenshot, cursor_coords):
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
        playfield_matrices = np.zeros((AMOUNT.PLAYFIELD_ROWS, AMOUNT.PLAYFIELD_COLUMNS, AMOUNT.TILE_TYPES))

        start_x = PIXELSIZE.TILE_WIDTH / 2
        start_y = (cursor_coords[1] + (PIXELSIZE.CURSOR_HEIGHT / 2)) % PIXELSIZE.TILE_HEIGHT
        # Loop over all blocks
        current_row = 0
        current_column = 0

        while current_row < AMOUNT.PLAYFIELD_ROWS:
            while current_column < AMOUNT.PLAYFIELD_COLUMNS:
                tile_x = int(start_x + (current_column * PIXELSIZE.TILE_WIDTH))
                tile_y = int(start_y + (current_row * PIXELSIZE.TILE_HEIGHT))
                tile_type = ImageProcessor.determine_tile_type(screenshot[tile_y, tile_x])
                if tile_type is not None:
                    playfield_matrices[current_row, current_column, tile_type] = 1
                current_column += 1
            current_row += 1
            current_column = 0

        return playfield_matrices

    def get_state(self):
        while True:
            gamewindow = screencapturer.capture_gamewindow()
            playfields = ImageProcessor.extract_playfields_from_gamewindow(gamewindow)
            cursor_coords = [None, None]
            cursor_position = [None, None]
            playfield_matrices = [None, None]
            game_active = [False, False]

            for player in PLAYERS:
                cursor_coords_player = ImageProcessor.determine_cursor_coords(playfields[player])
                if cursor_coords_player is not None:
                    cursor_coords[player] = cursor_coords_player
                    cursor_position_player = ImageProcessor.determine_cursor_position(cursor_coords[player])

                    if cursor_position_player is not None:
                        cursor_position[player] = cursor_position_player

                        playfield_matrices_player = ImageProcessor.determine_playfield_matrices(playfields[player], cursor_coords[player])
                        if np.sum(playfield_matrices_player[:, :, PANELS]) > 0:
                            playfield_matrices[player] = playfield_matrices_player
                            game_active[player] = True

            state = gamestate.GameState()
            state.playfield_matrices = playfield_matrices
            state.cursor_position = cursor_position
            state.game_active = game_active

            return state
