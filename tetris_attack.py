import sys
import subprocess
import time

LINUX = 'linux'
WINDOWS = 'windows'
SINGLE_PLAYER = 'single_player'
VS = 'vs'

EMULATOR_PATH = 'nintendo/windows/snes9x-x64.exe'
ROM_PATH = 'nintendo/tetris_attack.smc'
VS_SAVEGAME = 'nintendo/saves/Tetris Attack (U).000'
MULTIPLAYER_SAVEGAME = 'nintendo/saves/Tetris Attack (U).001'

def main(argv):
    os, player_mode, bot1, bot2 = parse_args(argv)
    start_game(os=os, player_mode=player_mode)
    # start_bots(os=os, bot1=bot1, bot2=bot2)


def parse_args(argv):
    if len(argv) < 3:
        raise Exception('Usage: main_old.py os player_mode bot1 [bot2]')

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
        return

    if os == WINDOWS:
        start_game_windows(player_mode)
        return

    raise Exception('Unexpected os: {}'.format(os))


def start_game_linux(player_mode):
    print('start game linux')

def start_game_windows(player_mode):
    subprocess.Popen([EMULATOR_PATH, ROM_PATH])

    time.sleep(2)

    if player_mode == VS:
        # press_key("F1")
        pass
    elif player_mode == SINGLE_PLAYER:
        # press_key("F2")
        pass



if __name__ == '__main__':
    main(sys.argv)