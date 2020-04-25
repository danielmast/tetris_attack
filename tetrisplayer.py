import numpy as np

# Actions
MOVE_UP = 1
MOVE_DOWN = 2
MOVE_LEFT = 3
MOVE_RIGHT = 4
SWAP = 5
STACK_UP = 6
DO_NOTHING = 7

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

PANELS = [PANEL_PURPLE, PANEL_YELLOW, PANEL_GREEN, PANEL_AQUAMARINE, PANEL_RED, PANEL_GREY, PANEL_BLUE]
GARBAGE = [GARBAGE_CONCRETE, GARBAGE_STEEL]

class TetrisPlayer():
    action_log = []

    def __init__(self):
        self.action_log = [DO_NOTHING]

    def find_top_row(self, playfield_matrices):
        channel_max = np.amax(playfield_matrices, axis=2)
        column_max = np.amax(channel_max, axis=1)
        indices = np.where(column_max == 1)

        return indices

    def find_panels_top_row(self, playfield_matrices):
        panel_matrices = playfield_matrices[:, :, PANELS]
        panels_top_row = self.find_top_row(panel_matrices)

        return panels_top_row

    def determine_mistakes(self, playfield_matrices, cursor_position):

    def determine_next_action(self, playfield_matrices, cursor_position):
        return MOVE_DOWN