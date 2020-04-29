# Standard library imports
import random
import platform

# Third party imports
import numpy as np

# Local application imports
from bot.bot import Bot
from constants import *
if platform.system().lower() == OS.WINDOWS:
    from input.windows import WindowsInput as Input
elif platform.system().lower() == OS.LINUX:
    from input.linux import LinuxInput as Input

class Laurens(Bot):
    def __init__(self, player):
        super().__init__(player)
        self.state = None
        self.player = player
        self.playfield_matrices = None
        self.cursor_position = None
        self.game_active = None
        self.input = Input()

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state):
        self.__state = state

    @staticmethod
    def find_tiles_top_row(playfield_matrices):
        tile_in_matrix = np.amax(playfield_matrices, axis=2)
        tile_in_row = np.amax(tile_in_matrix, axis=1)
        row_indices = np.where(tile_in_row == 1)

        if len(row_indices[0]) > 0:
            return row_indices[0][0]
        else:
            return None

    @staticmethod
    def find_panels_top_row(playfield_matrices):
        panels_matrices = playfield_matrices[:, :, PANELS]
        return Laurens.find_tiles_top_row(panels_matrices)

    @staticmethod
    def find_combinations_by_line(panel_in_line):
        # Preparation
        x = panel_in_line
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
    def find_closest_unobstructed_panel_in_row(starting_column, target_panel_row, panel_row, tile_row):
        column_offset = 1
        orientation_blocked = np.zeros((3,))
        while column_offset < AMOUNT.PLAYFIELD_COLUMNS:
            for orientation in ORIENTATIONS:
                if orientation_blocked[orientation] == 0:
                    search_column = starting_column + (column_offset * orientation)
                    if search_column in range(0, AMOUNT.PLAYFIELD_COLUMNS):
                        if tile_row[search_column] == 1 and panel_row[search_column] == 0:
                            orientation_blocked[orientation] = 1
                        else:
                            if target_panel_row[search_column] == 1:
                                return search_column
                    else:
                        orientation_blocked[orientation] = 1

            column_offset += 1

    @staticmethod
    def find_combinations_in_row(panel_matrix):
        # Find combinations
        row_sums = np.sum(panel_matrix, axis=1)
        row_indices = np.where(row_sums >= 3)[0]

        # Return results
        combinations_line = np.empty((2, len(row_indices)))
        combinations_line[0] = row_indices
        combinations_line[1] = row_sums[row_indices]
        return combinations_line

    @staticmethod
    def check_if_combinations_present(combinations):
        for orientation in ORIENTATIONS:
            for panel in PANELS:
                if np.nonzero(combinations[orientation][panel]):
                    return True

        return False

    @staticmethod
    def find_combinations_by_matrices(panels_matrices):
        combinations = []
        for orientation in ORIENTATIONS:
            combinations_panels = []
            for panel in PANELS:
                panel_matrix = panels_matrices[:, :, panel]

                if orientation == ORIENTATION.COLUMN:
                    panel_in_line = np.amax(panel_matrix, axis=orientation)
                    combinations_panels.append(Laurens.find_combinations_by_line(panel_in_line))

                if orientation == ORIENTATION.ROW:
                    combinations_panels.append(Laurens.find_combinations_in_row(panel_matrix))
            combinations.append(combinations_panels)
        return combinations


    @staticmethod
    def find_best_combination(combinations, playfield_matrices):
        best_combination_size = 0
        best_combination_orientation = None
        best_combination_panel = None
        best_combination_index = None

        # Combination in the top row for panels
        panels_top_combination_size = 0
        panels_top_combination_orientation = None
        panels_top_combination_panel = None
        panels_top_combination_index = None

        for orientation in ORIENTATIONS:
            orientation_results = combinations[orientation]
            for panel in PANELS:
                line_results = orientation_results[panel]
                if line_results[1].size > 0:  # Check if array is empty
                    best_size_in_line = np.amax(np.array(line_results[1]))

                    if best_size_in_line > best_combination_size:
                        indices = np.where(line_results[1] == best_size_in_line)
                        index = indices[0][0]
                        best_combination_orientation = orientation
                        best_combination_size = best_size_in_line
                        best_combination_panel = panel
                        best_combination_index = np.array(line_results[0])[index]

                        if best_combination_index == Laurens.find_panels_top_row(playfield_matrices):
                            panels_top_combination_orientation = best_combination_orientation
                            panels_top_combination_size = best_combination_size
                            panels_top_combination_panel = best_combination_panel
                            panels_top_combination_index = best_combination_index

        if Laurens.find_tiles_top_row(playfield_matrices) < Laurens.find_panels_top_row(playfield_matrices) and panels_top_combination_size > 0:  # Clean garbage combination
            return panels_top_combination_orientation, panels_top_combination_size, panels_top_combination_panel, panels_top_combination_index
        else:
            return best_combination_orientation, best_combination_size, best_combination_panel, best_combination_index

    @staticmethod
    def find_lowest_empty_tile_row(playfield_matrices):
        tile_in_matrix = np.sum(playfield_matrices, axis=2)
        tiles_in_row = np.sum(tile_in_matrix, axis=1)
        empty_tile_in_row_indices = np.where(tiles_in_row < AMOUNT.PLAYFIELD_COLUMNS)

        lowest_empty_tile_row = None
        if len(empty_tile_in_row_indices[0]) > 0:
            lowest_empty_tile_row = empty_tile_in_row_indices[0][-1]

        return lowest_empty_tile_row

    @staticmethod
    def find_panel_to_fill_the_gap(lowest_empty_tile_row, playfield_matrices):
        tile_in_matrix = np.sum(playfield_matrices, axis=2)
        panel_matrices = playfield_matrices[:, :, PANELS]
        panel_in_matrix = np.sum(panel_matrices, axis=2)

        fill_gap_row = lowest_empty_tile_row - 1
        origin_column = None
        target_column = None

        empty_tile_column_counter = 0
        while empty_tile_column_counter < AMOUNT.PLAYFIELD_COLUMNS:
            if tile_in_matrix[lowest_empty_tile_row, empty_tile_column_counter] == 0:
                target_panel_row = panel_in_matrix[fill_gap_row, :]
                panel_row = target_panel_row
                tile_row = tile_in_matrix[fill_gap_row, :]
                origin_column = Laurens.find_closest_unobstructed_panel_in_row(empty_tile_column_counter, target_panel_row, panel_row, tile_row)

                if origin_column is not None:
                    target_column = empty_tile_column_counter
                    return fill_gap_row, origin_column, fill_gap_row, target_column
            empty_tile_column_counter += 1

    @staticmethod
    def print_combination(combination):
        panel_name = ""
        if combination[2] == TILE.PURPLE:
            panel_name = "Purple"
        elif combination[2] == TILE.YELLOW:
            panel_name = "Yellow"
        elif combination[2] == TILE.GREEN:
            panel_name = "Green"
        elif combination[2] == TILE.AQUAMARINE:
            panel_name = "Aquamarine"
        elif combination[2] == TILE.RED:
            panel_name = "Red"
        elif combination[2] == TILE.GREY:
            panel_name = "Grey"
        elif combination[2] == TILE.BLUE:
            panel_name = "Blue"

        if combination[0] == ORIENTATION.ROW:
            orientation_name = "Rows"
        else:  # Columns
            orientation_name = "Columns"

        print("Combination -", "Orientation:", orientation_name, "Size:", combination[1], "Row start:", combination[3], "Panel:", panel_name)

    @staticmethod
    def print_tile_amounts(playfield_matrices):
        for tile in TILES:
            print("Tile", tile, ":", np.sum(playfield_matrices[:, :, tile]))

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
            return True

    def raise_stack(self):
        tiles_top_row = Laurens.find_tiles_top_row(self.playfield_matrices)
        tiles_top_row_expected = tiles_top_row
        panels_top_row = Laurens.find_panels_top_row(self.playfield_matrices)

        if tiles_top_row_expected > 6:
            while tiles_top_row_expected > 6:
                print("Stack up -", "Current row:", tiles_top_row_expected)
                self.input.do_action(self.player, ACTION.STACK_UP)
                tiles_top_row_expected -= 1
            return True

    def flatten_stack(self):
        playfield_matrices = self.playfield_matrices

        lowest_empty_tile_row = Laurens.find_lowest_empty_tile_row(playfield_matrices)
        panels_top_row = Laurens.find_panels_top_row(playfield_matrices)

        if lowest_empty_tile_row > panels_top_row:
            panel_to_fill_the_gap = Laurens.find_panel_to_fill_the_gap(lowest_empty_tile_row, playfield_matrices)

            if panel_to_fill_the_gap is not None:
                origin_position = [panel_to_fill_the_gap[0], panel_to_fill_the_gap[1]]
                target_position = [panel_to_fill_the_gap[2], panel_to_fill_the_gap[3]]
                print("Flatten stack -", "Origin:", origin_position, "Target:", target_position)
                return self.move_panel(origin_position, target_position)

    def make_column_combination(self, combination):
        combination_orientation, combination_size, combination_panel, combination_index = combination
        minimum_sizes = [3, 5, 4, 3, 3]
        offset = [0, 4, 3, 1, 2]

        # Calculate target row and column
        panel_matrix = self.playfield_matrices[:, :, combination_panel]
        target_row = int(combination_index)
        combination_size = int(combination_size)
        combination_matrix = panel_matrix[target_row:target_row + combination_size, :]
        combination_column_indices = np.where(combination_matrix == 1)
        combination_column_average = np.average(combination_column_indices[1])
        target_column = int(combination_column_average)

        # Minimize risk of accidental 3-combination
        if combination_size >= 4:
            while panel_matrix[target_row + 2, target_column] == 1:
                if target_column == 5:
                    target_column = 0
                else:
                    target_column += 1
        if combination_size > 4 and target_row + 5 < AMOUNT.PLAYFIELD_ROWS:
            while panel_matrix[target_row + 5, target_column] == 1:
                if target_column == 5:
                    target_column = 0
                else:
                    target_column += 1

        # A panel to the right position
        counter = 0
        while counter < len(minimum_sizes):
            if combination_size >= minimum_sizes[counter]:
                if panel_matrix[target_row + offset[counter], target_column] == 0:
                    target_panel_row = self.playfield_matrices[target_row + offset[counter], :, combination_panel]
                    panel_row = np.sum(self.playfield_matrices[target_row + offset[counter], :, PANELS], axis=1)
                    tile_row = np.sum(self.playfield_matrices[target_row + offset[counter], :, :], axis=1)
                    origin_column = Laurens.find_closest_unobstructed_panel_in_row(target_column, target_panel_row, panel_row, tile_row)
                    if origin_column is not None:
                        return self.move_panel(
                            origin_position=[target_row + offset[counter], origin_column],
                            target_position=[target_row + offset[counter], target_column]
                        )
            counter += 1

    def make_row_combination(self, combination):
        combination_orientation, combination_size, combination_panel, combination_index = combination
        sides_indices = [0, 2]
        offset = [-1, 1]

        panel_matrix = self.playfield_matrices[:, :, combination_panel]
        target_row = int(combination_index)
        panel_column_indices = np.where(panel_matrix[target_row, :] == 1)
        center_column = panel_column_indices[0][1]

        counter = 0
        while counter < len(sides_indices):
            if panel_matrix[target_row, center_column + offset[counter]] == 0:
                origin_column = panel_column_indices[0][sides_indices[counter]]
                return self.move_panel(
                    origin_position=[target_row, origin_column],
                    target_position=[target_row, center_column + offset[counter]]
                )
            counter += 1

    def make_largest_combination(self):
        panels_matrices = self.playfield_matrices[:, :, PANELS]
        combinations = Laurens.find_combinations_by_matrices(panels_matrices)

        if Laurens.check_if_combinations_present(combinations):
            best_combination = Laurens.find_best_combination(combinations, self.playfield_matrices)
            #Laurens.print_tile_amounts(self.playfield_matrices)
            best_combination_orientation, best_combination_size, best_combination_panel, best_combination_index = best_combination
            if best_combination_index is not None:
                Laurens.print_combination(best_combination)
                if best_combination_orientation == ORIENTATION.COLUMN:
                    return self.make_column_combination(best_combination)
                elif best_combination_orientation == ORIENTATION.ROW:
                    return self.make_row_combination(best_combination)

    def do_random_move(self):
        random_lower = 0
        if Laurens.find_panels_top_row(self.playfield_matrices) is not None:
            random_lower = Laurens.find_panels_top_row(self.playfield_matrices)

        random_row = random.randint(random_lower, AMOUNT.CURSOR_ROWS)
        random_origin_column = random.randint(0, AMOUNT.PLAYFIELD_COLUMNS / 2 - 1)
        random_target_column = random.randint(AMOUNT.PLAYFIELD_COLUMNS / 2, AMOUNT.PLAYFIELD_COLUMNS - 1)
        origin_position = [random_row, random_origin_column]
        target_position = [random_row, random_target_column]
        print("Random move -", "Origin:", origin_position, "Target:", target_position)
        return self.move_panel(origin_position, target_position)

    def start(self):
        while True:
            if self.state is not None:
                if self.state.game_active:
                    self.playfield_matrices = self.state.playfield_matrices[self.player]
                    self.cursor_position = self.state.cursor_position[self.player]
                    self.game_active = self.state.game_active

                    action_performed = self.raise_stack()
                    if not action_performed:
                        action_performed = self.flatten_stack()
                    if not action_performed:
                        action_performed = self.make_largest_combination()
                    if not action_performed:
                        action_performed = self.do_random_move()
