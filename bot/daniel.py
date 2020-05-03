# Standard library imports
import platform

import numpy as np
from tensorflow.keras.models import load_model

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
        self.model = load_model('bot/model.h5')

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state):
        self.__state = state

    def start(self):
        while True:
            if self.state is not None:
                if self.state.game_active[self.player]:
                    self.playfield_matrices = self.state.playfield_matrices[self.player]
                    self.cursor_position = self.state.cursor_position[self.player]
                    self.game_active = self.state.game_active[self.player]

                    sub_matrices = self.playfield_matrices[:,:,0:9]
                    prediction = self.model.predict(sub_matrices.reshape(1,648))
                    prediction = prediction.reshape(12, 6)
                    prediction_max = np.max(prediction)
                    prediction_boolean = (prediction == prediction_max)
                    indices = np.nonzero(prediction_boolean)

                    predicted_position = (indices[1][0], indices[0][0])

                    self.move_cursor(predicted_position)
                    self.input.do_action(self.player, ACTION.SWITCH_PANELS)


    def move_cursor(self, target_position):
        cursor_expected_position = list(self.cursor_position)

        while cursor_expected_position[0] < target_position[0]:
            self.input.do_action(self.player, ACTION.MOVE_DOWN)
            cursor_expected_position[0] += 1

        while cursor_expected_position[0] > target_position[0]:
            self.input.do_action(self.player, ACTION.MOVE_UP)
            cursor_expected_position[0] -= 1

        while cursor_expected_position[1] < target_position[1]:
            self.input.do_action(self.player, ACTION.MOVE_RIGHT)
            cursor_expected_position[1] += 1

        while cursor_expected_position[1] > target_position[1]:
            self.input.do_action(self.player, ACTION.MOVE_LEFT)
            cursor_expected_position[1] -= 1