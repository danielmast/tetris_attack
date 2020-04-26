# Standard library imports
import random

# Third party imports
import numpy as np

# Local application imports
from bot.bot import Bot
import tetrisgame as game


class Laurens(Bot):
    action_log = []
    planned_actions = []

    def __init__(self):
        super().__init__('laurens')
        self.action_log = [game.ACTION.DO_NOTHING]

    @staticmethod
    def find_tiles_top_row(playfield_matrices):
        channel_max = np.amax(playfield_matrices, axis=2)
        column_max = np.amax(channel_max, axis=1)
        row_indices = np.where(column_max == 1)

        if len(row_indices[0]) > 0:
            return row_indices[0][0]
        else:
            return None

    @staticmethod
    def find_panels_top_row(playfield_matrices):
        panel_matrices = playfield_matrices[:, :, game.PANELS]
        panels_top_row = Laurens.find_tiles_top_row(panel_matrices)

        return panels_top_row

    def determine_planned_actions(self):
        if len(self.planned_actions) > 0:
            return self.planned_actions.pop(0)

    def determine_mistakes(self):
        panels_matrices = game.playfield_matrices[:, :, game.PANELS]
        panels_top_row = Laurens.find_panels_top_row(game.playfield_matrices)
        tiles_top_row = Laurens.find_tiles_top_row(game.playfield_matrices)
        garbage_rows = panels_top_row - tiles_top_row

        # Cursor above top panel
        if game.cursor_position[0] < panels_top_row:
            return game.ACTION.MOVE_DOWN
        # Not enough tiles
        elif panels_top_row > 7:
            if tiles_top_row > 5:
                return game.ACTION.STACK_UP
            elif panels_top_row > 9 and tiles_top_row > 2:
                return game.ACTION.STACK_UP
        # Tower
        elif panels_top_row <= 5 and np.sum(panels_matrices[panels_top_row:panels_top_row + 3, :, :]) <= 9:
            # Remove tower
            print("Tiles in top 3 rows", np.sum(panels_matrices[panels_top_row:panels_top_row + 3, :, :]))
        # Dangerous garbage
        elif garbage_rows >= 5 or (garbage_rows > 0 and tiles_top_row < 2):
            # Remove garbage
            print("Garbage rows", garbage_rows)

    def determine_combinations(self):
        return None

    def determine_default_behavior(self):
        if self.action_log[-1] != game.ACTION.SWITCH_PANELS:
            return game.ACTION.SWITCH_PANELS
        else:
            return random.choice(game.MOVES)

    def get_action(self):
        action = self.determine_planned_actions()
        if action is None:
            action = self.determine_mistakes()
        if action is None:
            action = self.determine_combinations()
        if action is None:
            action = self.determine_default_behavior()

        self.action_log.append(action)

        return action