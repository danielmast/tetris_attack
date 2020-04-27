# Standard library imports
import random
import platform

# Third party imports
import numpy as np

# Local application imports
from bot.bot import Bot
import constants
if platform.system().lower() == constants.OS.WINDOWS:
    import input.windows as input
elif platform.system().lower() == constants.OS.LINUX:
    import input.linux as input


class Laurens(Bot):
    def __init__(self, player):
        super().__init__(player)
        self.player = player
        self.action_log = [constants.ACTION.DO_NOTHING]
        self.planned_actions = []
        self.playfield_matrices = None
        self.cursor_position = None

    def find_tiles_top_row(self, panels_only=False):
        playfield_matrices = self.playfield_matrices

        if panels_only:
            playfield_matrices = self.playfield_matrices[:, :, constants.PANELS]

        channel_max = np.amax(playfield_matrices, axis=2)
        column_max = np.amax(channel_max, axis=1)
        row_indices = np.where(column_max == 1)

        if len(row_indices[0]) > 0:
            return row_indices[0][0]
        else:
            return None

    def find_panels_top_row(self):
        return self.find_tiles_top_row(panels_only=True)

    def determine_planned_actions(self):
        if len(self.planned_actions) > 0:
            return self.planned_actions.pop(0)

    def determine_mistakes(self):
        panels_matrices = self.playfield_matrices[:, :, constants.PANELS]
        panels_top_row = self.find_panels_top_row()
        tiles_top_row = self.find_tiles_top_row()
        garbage_rows = panels_top_row - tiles_top_row

        # Cursor above top panel
        if self.cursor_position[0] < panels_top_row:
            return constants.ACTION.MOVE_DOWN
        # Not enough tiles
        elif panels_top_row > 7:
            if tiles_top_row > 5:
                return constants.ACTION.STACK_UP
            elif panels_top_row > 9 and tiles_top_row > 2:
                return constants.ACTION.STACK_UP
        # Tower
        elif panels_top_row <= 5 and np.sum(panels_matrices[panels_top_row:panels_top_row + 3, :, :]) <= 9:
            # Remove tower
            #print("Tiles in top 3 rows", np.sum(panels_matrices[panels_top_row:panels_top_row + 3, :, :]))
            pass
        # Dangerous garbage
        elif garbage_rows >= 5 or (garbage_rows > 0 and tiles_top_row < 2):
            # Remove garbage
            #print("Garbage rows", garbage_rows)
            pass

    def determine_combinations(self):
        return None

    def determine_default_behavior(self):
        if self.action_log[-1] != constants.ACTION.SWITCH_PANELS:
            return constants.ACTION.SWITCH_PANELS
        else:
            return random.choice(constants.MOVES)

    def do_action(self, state):
        if state is not None:
            self.playfield_matrices = state.playfield_matrices[self.player]
            self.cursor_position = state.cursor_position[self.player]

            action = self.determine_planned_actions()
            if action is None:
                action = self.determine_mistakes()
            if action is None:
                action = self.determine_combinations()
            if action is None:
                action = self.determine_default_behavior()

            self.action_log.append(action)

            # Perform action
            input.do_action(self.player, action)
