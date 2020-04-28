# Standard library imports
import platform
import random

# Local application imports
from bot.bot import Bot
from constants import OS, ACTION
if platform.system().lower() == OS.WINDOWS:
    from input.windows import WindowsInput as Input
elif platform.system().lower() == OS.LINUX:
    from input.linux import LinuxInput as Input


class Daniel(Bot):
    def __init__(self, player):
        super().__init__(player)
        self.player = player
        self.playfield_matrices = None
        self.cursor_position = None
        self.input = Input()

    def do_action(self, state):
        if state is not None:
            self.playfield_matrices = state.playfield_matrices[self.player]
            self.cursor_position = state.cursor_position[self.player]

            # Perform random action
            action = random.choice([ACTION.SWITCH_PANELS, ACTION.MOVE_UP, ACTION.MOVE_DOWN, ACTION.MOVE_LEFT, ACTION.MOVE_RIGHT])
            self.input.do_action(self.player, action)
