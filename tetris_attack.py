import sys
import platform
import emulator
import bots

LINUX = 'linux'
WINDOWS = 'windows'
SINGLE_PLAYER = 'single_player'
VS = 'vs'


def main(argv):
    player_mode, bot1, bot2 = parse_args(argv)
    os = platform.system().lower()
    emulator.start_game(os=os)
    emulator.load_game(player_mode=player_mode)
    bots.start_bots(os=os, bot1=bot1, bot2=bot2)


def parse_args(argv):
    if len(argv) < 2:
        raise Exception('Usage: python tetris_attack.py player_mode bot1 [bot2]')

    player_mode = argv[2]
    if player_mode != SINGLE_PLAYER and player_mode != VS:
        raise Exception('player_mode should be {} or {}'.format(SINGLE_PLAYER, VS))

    bot1 = argv[2]

    bot2 = None
    if (len(argv) == 4):
        bot2 = argv[3]

    return player_mode, bot1, bot2


if __name__ == '__main__':
    main(sys.argv)
