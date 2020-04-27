class GameState():
    def __init__(self, playfield_matrices=None, cursor_position=None, game_active=None):
        self.playfield_matrices = playfield_matrices
        self.cursor_position = cursor_position
        self.game_active = game_active

    @property
    def playfield_matrices(self):
        return self.__playfield_matrices

    @property
    def cursor_position(self):
        return self.__cursor_position

    @property
    def game_active(self):
        return self.__game_active

    @playfield_matrices.setter
    def playfield_matrices(self, playfield_matrices):
        self.__playfield_matrices = playfield_matrices

    @cursor_position.setter
    def cursor_position(self, cursor_position):
        self.__cursor_position = cursor_position

    @game_active.setter
    def game_active(self, game_active):
        self.__game_active = game_active
