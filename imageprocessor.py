# Standard library imports
import math
import time
import platform

# Third party imports
import cv2
import numpy as np

# Local application imports
import constants
import gamestate
if platform.system().lower() == constants.OS.WINDOWS:
    import screencapturer.windows as screencapturer
elif platform.system().lower() == constants.OS.LINUX:
    import screencapturer.linux as screencapturer


class ImageProcessor():
    @staticmethod
    def extract_playfields_from_gamewindow(gamewindow):
        playfields = []

        if gamewindow.shape[1] > constants.PIXELSIZE.GAMEWINDOW_WIDTH:
            gamewindow_offset_y = constants.PIXELSIZE.GAMEWINDOW_OFFSET_Y
            gamewindow_offset_x = constants.PIXELSIZE.GAMEWINDOW_OFFSET_X
        else:
            gamewindow_offset_y = 0
            gamewindow_offset_x = 0

        y1 = gamewindow_offset_y + constants.PIXELSIZE.PLAYFIELD_OFFSET_Y
        y2 = y1 + constants.PIXELSIZE.PLAYFIELD_HEIGHT
        x1_p1 = gamewindow_offset_x + constants.PIXELSIZE.PLAYFIELD_OFFSET_X_P1
        x2_p1 = x1_p1 + constants.PIXELSIZE.PLAYFIELD_WIDTH
        x1_p2 = gamewindow_offset_x + constants.PIXELSIZE.PLAYFIELD_OFFSET_X_P2
        x2_p2 = x1_p2 + constants.PIXELSIZE.PLAYFIELD_WIDTH

        playfields.append(gamewindow[y1:y2, x1_p1:x2_p1])
        playfields.append(gamewindow[y1:y2, x1_p2:x2_p2])

        return playfields

    @staticmethod
    def determine_cursor_coords(playfield):
        offset_x = -12
        offset_y = 1

        template = np.load('npy/cursor_center.npy')
        screenshot_gray = cv2.cvtColor(np.array(playfield), cv2.COLOR_RGB2GRAY)

        result = cv2.matchTemplate(screenshot_gray, template, method=cv2.TM_CCOEFF)
        min_value, max_value, min_coords, max_coords = cv2.minMaxLoc(result)

        cursor_start_x = max_coords[0] + offset_x
        cursor_start_y = max_coords[1] + offset_y
        cursor_end_x = cursor_start_x + constants.PIXELSIZE.CURSOR_WIDTH
        cursor_end_y = cursor_start_y + constants.PIXELSIZE.CURSOR_HEIGHT

        return [cursor_start_x, cursor_start_y, cursor_end_x, cursor_end_y]

    @staticmethod
    def determine_cursor_position(cursor_coords):
        offset_row = 0
        offset_column = 0

        cursor_row = math.floor((cursor_coords[1] + (constants.PIXELSIZE.TILE_HEIGHT / 2)) / constants.PIXELSIZE.TILE_HEIGHT) + offset_row
        cursor_column = math.floor((cursor_coords[0] + (constants.PIXELSIZE.TILE_WIDTH / 2)) / constants.PIXELSIZE.TILE_WIDTH) + offset_column

        return cursor_row, cursor_column

    @staticmethod
    def determine_tile_type(pixel):
        color_string = " ".join(map(str, (list(pixel))))

        if color_string in constants.COLOR_TILE_MAPPING:
            return constants.COLOR_TILE_MAPPING[color_string]
        else:
            return None

    @staticmethod
    def determine_playfield_matrices(screenshot, cursor_coords):
        playfield_matrices = np.zeros((constants.AMOUNT.PLAYFIELD_ROWS, constants.AMOUNT.PLAYFIELD_COLUMNS, constants.AMOUNT.TILE_TYPES))

        start_x = round(constants.PIXELSIZE.TILE_WIDTH / 2)
        start_y = (cursor_coords[1] + round(constants.PIXELSIZE.CURSOR_HEIGHT / 2)) % constants.PIXELSIZE.TILE_HEIGHT

        # Loop over all blocks
        current_row = 0
        current_column = 0
        while current_row < constants.AMOUNT.PLAYFIELD_ROWS:
            while current_column < constants.AMOUNT.PLAYFIELD_COLUMNS:
                tile_x = int(start_x + (current_column * constants.PIXELSIZE.TILE_WIDTH))
                tile_y = int(start_y + (current_row * constants.PIXELSIZE.TILE_HEIGHT))
                tile_type = ImageProcessor.determine_tile_type(screenshot[tile_y, tile_x])
                if tile_type is not None:
                    playfield_matrices[current_row, current_column, tile_type] = 1
                current_column += 1
            current_row += 1
            current_column = 0

        return playfield_matrices

    def start(self):
        while True:
            state = gamestate.GameState()
            gamewindow = screencapturer.capture_gamewindow()
            playfields = ImageProcessor.extract_playfields_from_gamewindow(gamewindow)
            cursor_coords = []
            cursor_position = []
            playfield_matrices = []

            for player in constants.PLAYERS:
                cursor_coords.append(ImageProcessor.determine_cursor_coords(playfields[player]))
                cursor_position.append(ImageProcessor.determine_cursor_position(cursor_coords[player]))
                playfield_matrices.append(ImageProcessor.determine_playfield_matrices(playfields[player], cursor_coords[player]))
                print(cursor_position[player])

            state.playfield_matrices = playfield_matrices
            state.cursor_position = cursor_position
            state.game_active = True


ip = ImageProcessor()
ip.start()