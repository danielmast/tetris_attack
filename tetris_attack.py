# Standard library imports
import sys
import platform
import threading
import multiprocessing

# Local application imports
import emulator
import imageprocessor
import constants
import gamestate
from bot.laurens import Laurens
from bot.daniel import Daniel

state = None


def main(argv):
    #player_mode, bot1, bot2 = parse_args(argv)
    #os = platform.system().lower()
    #emulator.start_game(os=os)
    #emulator.load_game(player_mode=player_mode)

    state = gamestate.GameState()
    shared_memory = multiprocessing.shared_memory.SharedMemory(create=True, size=3e6)

    ip = imageprocessor.ImageProcessor(shared_memory)
    bot1 = Daniel(constants.PLAYER.ONE)
    bot2 = Laurens(constants.PLAYER.TWO)

    threading.Thread(target=ip.start()).start()
    threading.Thread(target=bot1.start()).start()
    threading.Thread(target=bot2.start()).start()

    #bots.start_bots(os=os, bot1_name=bot1, bot2_name=bot2)


def parse_args(argv):
    if len(argv) < 3:
        raise Exception('Usage: python tetris_attack.py player_mode bot1 [bot2]')

    player_mode = argv[1]
    if player_mode != constants.GAMEMODE.SINGLE_PLAYER and player_mode != constants.GAMEMODE.VS:
        raise Exception('player_mode should be {} or {}'.format(constants.GAMEMODE.SINGLE_PLAYER, constants.GAMEMODE.VS))

    bot1 = argv[2]

    bot2 = None
    if len(argv) == 4:
        bot2 = argv[3]

    return player_mode, bot1, bot2


if __name__ == '__main__':
    main(sys.argv)
