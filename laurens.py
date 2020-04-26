# Standard library imports
from enum import Enum

# Third party imports
import numpy as np
import random

# Local application imports
from bot import Bot


# Actions
MOVE_UP = 1
MOVE_DOWN = 2
MOVE_LEFT = 3
MOVE_RIGHT = 4
SWITCH_PANELS = 5
STACK_UP = 6
DO_NOTHING = 7

# Action groups
MOVES = [MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT]


class Laurens(Bot):
    action_log = []
    planned_actions = []
    TILES = []
    PANELS = []
    GARBAGE = []

    def __init__(self, tiles):
        super().__init__('laurens')
        self.action_log = [DO_NOTHING]
        self.TILES = tiles
        self.PANELS = [
            tiles['PURPLE'],
            tiles['YELLOW'],
            tiles['GREEN'],
            tiles['AQUAMARINE'],
            tiles['RED'],
            tiles['GREY'],
            tiles['BLUE']
        ]
        self.GARBAGE = [
            tiles['CONCRETE'],
            tiles['STEEL']
        ]

    def find_tiles_top_row(self, playfield_matrices):
        channel_max = np.amax(playfield_matrices, axis=2)
        column_max = np.amax(channel_max, axis=1)
        row_indices = np.where(column_max == 1)

        if len(row_indices[0]) > 0:
            return row_indices[0][0]
        else:
            return None

    def find_panels_top_row(self, playfield_matrices):
        panel_matrices = playfield_matrices[:, :, self.PANELS]
        panels_top_row = self.find_tiles_top_row(panel_matrices)

        return panels_top_row

    def determine_planned_actions(self):
        if len(self.planned_actions) > 0:
            return self.planned_actions.pop(0)

    def determine_mistakes(self, playfield_matrices, cursor_position):
        panels_matrices = playfield_matrices[:, :, self.PANELS]
        panels_top_row = self.find_panels_top_row(playfield_matrices)
        tiles_top_row = self.find_tiles_top_row(playfield_matrices)
        garbage_rows = panels_top_row - tiles_top_row

        # Cursor above top panel
        if cursor_position[0] < panels_top_row:
            return MOVE_DOWN
        # Not enough tiles
        elif panels_top_row > 7:
            if tiles_top_row > 5:
                return STACK_UP
            elif panels_top_row > 9 and tiles_top_row > 2:
                return STACK_UP
        # Tower
        elif panels_top_row <= 5 and np.sum(panels_matrices[panels_top_row:panels_top_row + 3, :, :]) <= 9:
            # Remove tower
            print("Tiles in top 3 rows", np.sum(panels_matrices[panels_top_row:panels_top_row + 3, :, :]))
        # Dangerous garbage
        elif garbage_rows >= 5 or (garbage_rows > 0 and tiles_top_row < 2):
            # Remove garbage
            print("Garbage rows", garbage_rows)

    def determine_combinations(self, playfield_matrices, cursor_position):
        return None

    def determine_default_behavior(self, playfield_matrices, cursor_position):
        if self.action_log[-1] != SWITCH_PANELS:
            return SWITCH_PANELS
        else:
            return random.choice(MOVES)

    def get_action(self, playfield_matrices, cursor_position):
        action = self.determine_planned_actions()
        if action is None:
            action = self.determine_mistakes(playfield_matrices, cursor_position)
        if action is None:
            action = self.determine_combinations(playfield_matrices, cursor_position)
        if action is None:
            action = self.determine_default_behavior(playfield_matrices, cursor_position)

        self.action_log.append(action)

        return action
