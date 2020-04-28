# Standard library imports
import random
import platform

# Third party imports
import numpy as np

# Local application imports
from bot.bot import Bot
from constants import OS, ACTION, ORIENTATION, PANELS, TILE
if platform.system().lower() == OS.WINDOWS:
    from input.windows import WindowsInput as Input
elif platform.system().lower() == OS.LINUX:
    from input.linux import LinuxInput as Input


class Laurens(Bot):
    def __init__(self, player):
        super().__init__(player)
        self.player = player
        self.playfield_matrices = None
        self.cursor_position = None
        self.input = Input()

    def find_tiles_top_row(self, panels_only=False):
        playfield_matrices = self.playfield_matrices

        if panels_only:
            playfield_matrices = self.playfield_matrices[:, :, PANELS]

        channel_max = np.amax(playfield_matrices, axis=2)
        column_max = np.amax(channel_max, axis=1)
        row_indices = np.where(column_max == 1)

        if len(row_indices[0]) > 0:
            return row_indices[0][0]
        else:
            return None

    def find_panels_top_row(self):
        return self.find_tiles_top_row(panels_only=True)

    @staticmethod
    def find_combinations_by_line(present_in_line):
        # Preparation
        x = present_in_line
        n = x.shape[0]

        # Find run starts, values and lengths
        loc_combination_start = np.empty(n, dtype=bool)
        loc_combination_start[0] = True
        np.not_equal(x[:-1], x[1:], out=loc_combination_start[1:])
        combination_starts = np.nonzero(loc_combination_start)[0]
        combination_values = x[loc_combination_start]
        combination_size = np.diff(np.append(combination_starts, n))

        # Filter valid combinations
        combination_filter = np.logical_and(combination_values == 1, combination_size >= 3)

        # Return results
        combinations_line = np.empty((2, np.count_nonzero(combination_filter)))
        combinations_line[0] = combination_starts[combination_filter]
        combinations_line[1] = combination_size[combination_filter]
        return combinations_line

    @staticmethod
    def check_if_combinations_present(combinations):
        for panel in PANELS:
            if np.nonzero(combinations[panel]):
                return True

        return False

    @staticmethod
    def find_combinations_by_matrices(panels_matrices):
        combinations = []
        for panel in PANELS:
            panel_matrix = panels_matrices[:, :, panel]
            present_in_line = np.amax(panel_matrix, axis=ORIENTATION.COLUMN)
            combinations.append(Laurens.find_combinations_by_line(present_in_line))
        
        return combinations

    @staticmethod
    def find_best_combination(combinations):
        best_combination_size = 0
        best_combination_panel = None
        best_combination_index = None

        for panel in PANELS:
            line_results = combinations[panel]
            if line_results[1].size > 0: # Check if array is empty
                best_size_in_line = np.amax(np.array(line_results[1]))

                if best_size_in_line > best_combination_size:
                    indices = np.where(line_results[1] == best_size_in_line)
                    index = indices[0][0]
                    best_combination_size = best_size_in_line
                    best_combination_panel = panel
                    best_combination_index = np.array(line_results[0])[index]

        return best_combination_size, best_combination_panel, best_combination_index

    @staticmethod
    def print_combination(combination):
        panel_name = ""
        if combination[1] == TILE.PURPLE:
            panel_name = "Purple"
        elif combination[1] == TILE.YELLOW:
            panel_name = "Yellow"
        elif combination[1] == TILE.GREEN:
            panel_name = "Green"
        elif combination[1] == TILE.AQUAMARINE:
            panel_name = "Aquamarine"
        elif combination[1] == TILE.RED:
            panel_name = "Red"
        elif combination[1] == TILE.GREY:
            panel_name = "Grey"
        elif combination[1] == TILE.BLUE:
            panel_name = "Blue"
        print("Size:", combination[0], "Row start:", combination[2], "Panel:", panel_name)

    def move_panel(self, origin_position, target_position):
        if origin_position[1] != target_position[1]:    # Check if panel needs to move
            cursor_expected_position = list(self.cursor_position)
            offset_cursor = 0                           # Offset for moving right
            if origin_position[1] > target_position[1]:
                offset_cursor = 1                       # Offset for moving left

            while cursor_expected_position[0] < origin_position[0]:
                self.input.do_action(self.player, ACTION.MOVE_DOWN)
                cursor_expected_position[0] += 1

            while cursor_expected_position[0] > origin_position[0]:
                self.input.do_action(self.player, ACTION.MOVE_UP)
                cursor_expected_position[0] -= 1

            while cursor_expected_position[1] + offset_cursor > origin_position[1]:
                self.input.do_action(self.player, ACTION.MOVE_LEFT)
                cursor_expected_position[1] -= 1

            while cursor_expected_position[1] + offset_cursor < origin_position[1]:
                self.input.do_action(self.player, ACTION.MOVE_RIGHT)
                cursor_expected_position[1] += 1

            while cursor_expected_position[1] != target_position[1]:
                if cursor_expected_position[1] < target_position[1]:
                    self.input.do_action(self.player, ACTION.SWITCH_PANELS)
                    self.input.do_action(self.player, ACTION.MOVE_RIGHT)
                    cursor_expected_position[1] += 1
                elif cursor_expected_position[1] + offset_cursor > target_position[1]:
                    self.input.do_action(self.player, ACTION.SWITCH_PANELS)
                    self.input.do_action(self.player, ACTION.MOVE_LEFT)
                    cursor_expected_position[1] -= 1

            self.input.do_action(self.player, ACTION.SWITCH_PANELS)

    def make_largest_combination(self):
        panels_matrices = self.playfield_matrices[:, :, PANELS]

        combinations = Laurens.find_combinations_by_matrices(panels_matrices)
        if Laurens.check_if_combinations_present(combinations):
            best_combination = Laurens.find_best_combination(combinations)
            Laurens.print_combination(best_combination)
            best_combination_size, best_combination_panel, best_combination_index = best_combination
            if best_combination_size is not None and best_combination_panel is not None and best_combination_index is not None:
                minimum_sizes = [5, 4, 3, 3]
                offset = [4, 3, 1, 2]

                panel_matrix = self.playfield_matrices[:, :, best_combination_panel]
                target_row = int(best_combination_index)
                target_column_indices = np.where(panel_matrix[target_row, :] == 1)
                target_column = target_column_indices[0][0]

                counter = 0
                while counter < len(minimum_sizes):
                    if best_combination_size >= minimum_sizes[counter]:
                        if panel_matrix[target_row + offset[counter], target_column] == 0:
                            origin_column_indices = np.where(panel_matrix[target_row + offset[counter], :] == 1)
                            origin_column = origin_column_indices[0][0]
                            self.move_panel(
                                origin_position=[target_row + offset[counter], origin_column],
                                target_position=[target_row + offset[counter], target_column]
                            )
                            return True

                    counter += 1
                else:
                    return False
        else:
            return False

    def do_random_move(self):
        action = random.choice(
            [ACTION.SWITCH_PANELS, ACTION.MOVE_UP, ACTION.MOVE_DOWN, ACTION.MOVE_LEFT, ACTION.MOVE_RIGHT])
        self.input.do_action(self.player, action)

        return True

    def do_action(self, state):
        if state is not None:
            self.playfield_matrices = state.playfield_matrices[self.player]
            self.cursor_position = state.cursor_position[self.player]

            action_performed = self.make_largest_combination()
            if not action_performed:
                self.do_random_move()
