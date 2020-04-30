# Standard library imports
from subprocess import Popen, PIPE
import time

# Local application imports
from input.input import Input
from constants import PLAYER, ACTION_KEY_MAPPING_P1, ACTION_KEY_MAPPING_P2


class LinuxInput(Input):

    def __init__(self):
        super().__init__()
        self.window_id = LinuxInput.get_window_id()


    @staticmethod
    def get_key(player, action):
        if player == PLAYER.ONE:
            return ACTION_KEY_MAPPING_P1[action]
        elif player == PLAYER.TWO:
            return ACTION_KEY_MAPPING_P2[action]
        raise Exception('Unexpected player: {}'.format(player))

    @staticmethod
    def get_window_id():
        proc = Popen(["xdotool", "search", "ZSNES"], stdout=PIPE)
        out, err = proc.communicate()
        return out.decode('utf-8')[:-1]

    def key_press(self, key, sleep_after_key_press=2 / 60):
        Popen(["xdotool", "keydown", "-window", self.window_id, key], stdout=PIPE).communicate()
        Popen(["xdotool", "keyup", "-window", self.window_id, key], stdout=PIPE).communicate()
        time.sleep(sleep_after_key_press)

    def do_action(self, player, action):
        key = LinuxInput.get_key(player, action)
        self.key_press(key)
