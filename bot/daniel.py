# Local application imports
from bot.bot import Bot
import constants


class Daniel(Bot):
    def __init__(self, player):
        super().__init__(player)
        global state
        self.player = player
        self.playfield_matrices = state.playfield_matrices[player]
        self.cursor_position = state.cursor_position[player]

    def start(self):
        return constants.ACTION.MOVE_DOWN
