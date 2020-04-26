# Standard library imports
import time
import subprocess

# Constants
LINUX = 'linux'
WINDOWS = 'windows'
EMULATOR_PATH_LINUX = 'zsnes'
EMULATOR_PATH_WINDOWS = 'nintendo/windows/snes9x-x64.exe'
ROM_PATH = 'nintendo/tetris_attack.smc'


def start_game(os):
    if os == LINUX:
        subprocess.Popen([EMULATOR_PATH_LINUX, ROM_PATH])
    elif os == WINDOWS:
        subprocess.Popen([EMULATOR_PATH_WINDOWS, ROM_PATH])
    else:
        raise Exception('Unexpected os: {}'.format(os))

    time.sleep(2)


def load_game(player_mode):
    print ('load game with player_mode {}'.format(player_mode))