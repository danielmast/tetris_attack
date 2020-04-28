# Standard library imports
import time
import subprocess
import platform

# Local application imports
from constants import OS, EMULATOR, GAMEMODE
if platform.system().lower() == OS.WINDOWS:
    from input.windows import WindowsInput as Input
elif platform.system().lower() == OS.LINUX:
    from input.linux import LinuxInput as Input


def start_game(os):
    if os == OS.LINUX:
        subprocess.Popen([EMULATOR.PATH_LINUX, EMULATOR.ROM_PATH])
    elif os == OS.WINDOWS:
        subprocess.Popen([EMULATOR.PATH_WINDOWS, EMULATOR.ROM_FILENAME])
    else:
        raise Exception('Unexpected os: {}'.format(os))

    time.sleep(2)


def load_game(os, game_mode):
    input = Input()

    if os == OS.LINUX:
        input.press_key('F4')
    elif os == OS.WINDOWS:
        if game_mode == GAMEMODE.VS:
            input.press_key('F1')
        elif game_mode == GAMEMODE.SINGLE_PLAYER:
            input.press_key('F2')

    time.sleep(0.1)
