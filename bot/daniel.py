# Standard library imports
import platform

# Local application imports
from bot.bot import Bot
import constants
if platform.system().lower() == constants.OS.WINDOWS:
    import input.windows as input
elif platform.system().lower() == constants.OS.LINUX:
    import input.linux as input


class Daniel(Bot):
    def __init__(self, player):
        super().__init__(player)
        self.player = player
        self.playfield_matrices = None
        self.cursor_position = None

    def do_action(self, state):
        if state is not None:
            self.playfield_matrices = state.playfield_matrices[self.player]
            self.cursor_position = state.cursor_position[self.player]

            # Perform action
            action = constants.ACTION.MOVE_DOWN
            input.do_action(self.player, action)
