from input.input import Input
from pynput.keyboard import Controller
from constants import PLAYER, ACTION_KEY_MAPPING_P1, ACTION_KEY_MAPPING_P2

class LinuxInput(Input):

    def __init__(self):
        super().__init__()
        self.keyboard = Controller()

    @staticmethod
    def get_key(player, action):
        if player == PLAYER.ONE:
            return ACTION_KEY_MAPPING_P1[action]
        elif player == PLAYER.TWO:
            return ACTION_KEY_MAPPING_P2[action]
        raise Exception('Unexpected player: {}'.format(player))

    def do_action(self, player, action):
        key = LinuxInput.get_key(player, action)
        self.keyboard.press(key)
        self.keyboard.release(key)
