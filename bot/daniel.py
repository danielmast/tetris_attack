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

    def start(self):
        while True:
            if self.state is not None:
                if self.state.game_active:
                    self.playfield_matrices = self.state.playfield_matrices[self.player]
                    self.cursor_position = self.state.cursor_position[self.player]
                    self.game_active = self.state.game_active

                    # Perform random action
                    action = random.choice([ACTION.SWITCH_PANELS, ACTION.MOVE_UP, ACTION.MOVE_DOWN, ACTION.MOVE_LEFT, ACTION.MOVE_RIGHT])
                    self.input.do_action(self.player, action)
