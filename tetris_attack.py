import sys
import subprocess
import time

LINUX = 'linux'
WINDOWS = 'windows'
SINGLE_PLAYER = 'single_player'
VS = 'vs'

EMULATOR_PATH_LINUX = 'zsnes'
EMULATOR_PATH_WINDOWS = 'nintendo/windows/snes9x-x64.exe'
ROM_PATH = 'nintendo/tetris_attack.smc'

def main(argv):
    os, player_mode, bot1, bot2 = parse_args(argv)
    start_game(os=os, player_mode=player_mode)
    # start_bots(os=os, bot1=bot1, bot2=bot2)


def parse_args(argv):
    if len(argv) < 3:
        raise Exception('Usage: python tetris_attack.py os player_mode bot1 [bot2]')

    os = argv[1]
    if os != LINUX and os != WINDOWS:
        raise Exception('os should be {} or {}'.format(LINUX, WINDOWS))

    player_mode = argv[2]
    if player_mode != SINGLE_PLAYER and player_mode != VS:
        raise Exception('player_mode should be {} or {}'.format(SINGLE_PLAYER, VS))

    bot1 = argv[2]

    bot2 = None
    if (len(argv) == 4):
        bot2 = argv[3]

    return os, player_mode, bot1, bot2


def start_game(os, player_mode):
    if os == LINUX:
        start_game_linux(player_mode)
    elif os == WINDOWS:
        start_game_windows(player_mode)
    else:
        raise Exception('Unexpected os: {}'.format(os))

    time.sleep(2)


def start_game_linux(player_mode):
    subprocess.Popen([EMULATOR_PATH_LINUX, ROM_PATH])


def start_game_windows(player_mode):
    subprocess.Popen([EMULATOR_PATH_WINDOWS, ROM_PATH])


if __name__ == '__main__':
    main(sys.argv)
