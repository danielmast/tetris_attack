# Standard library imports
import sys
import platform
import threading
import multiprocessing

# Local application imports
import emulator
import imageprocessor
from constants import BOT, PLAYER, GAMEMODE
from bot.laurens import Laurens
from bot.daniel import Daniel


def get_bot(bot_name, player):
    if bot_name == BOT.LAURENS:
        return Laurens(player)
    elif bot_name == BOT.DANIEL:
        return Daniel(player)
    else:
        raise Exception("Unexpected bot name: {}".format(bot_name))


def start_imageprocessor(ip, bot1, bot2):
    while True:
        state = ip.get_state()
        bot1.state = state
        if bot2 is not None:
            bot2.state = state


def main(argv):
    game_mode, bot1_name, bot2_name = parse_args(argv)
    os = platform.system().lower()
    emulator.start_game(os=os)
    emulator.load_game(os=os, game_mode=game_mode)

    bot1 = get_bot(bot1_name, PLAYER.ONE)
    bot1_thread = threading.Thread(target=bot1.start)
    bot1_thread.start()

    bot2 = None
    if bot2_name is not None:
        bot2 = get_bot(bot2_name, PLAYER.TWO)
        bot2_thread = threading.Thread(target=bot2.start)
        bot2_thread.start()

    ip = imageprocessor.ImageProcessor()
    imageprocessor_thread = threading.Thread(target=start_imageprocessor, args=(ip, bot1, bot2))
    imageprocessor_thread.start()


def parse_args(argv):
    if len(argv) < 3:
        raise Exception('Usage: python tetris_attack.py game_mode bot1 [bot2]')

    game_mode = argv[1]
    if game_mode != GAMEMODE.SINGLE_PLAYER and game_mode != GAMEMODE.VS:
        raise Exception('game_mode should be {} or {}'.format(GAMEMODE.SINGLE_PLAYER, GAMEMODE.VS))

    bot1 = argv[2]

    bot2 = None
    if len(argv) == 4:
        bot2 = argv[3]

    return game_mode, bot1, bot2


if __name__ == '__main__':
    main(sys.argv)
