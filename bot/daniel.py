# Local application imports
from bot.bot import Bot
import constants


class Daniel(Bot):
    def __init__(self, player):
        super().__init__(player)
        global state
        self.player = player
        self.playfield_matrices = None
        self.cursor_position = None

    def get_action(self, state):
        if state is not None:
            self.playfield_matrices = state.playfield_matrices[self.player]
            self.cursor_position = state.cursor_position[self.player]
            return constants.ACTION.MOVE_DOWN
        else:
            return constants.ACTION.DO_NOTHING
