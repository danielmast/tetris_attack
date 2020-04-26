# Standard library imports
import time

# Local application imports
from laurens import Laurens
from daniel import Daniel

# Constants
LAURENS = 'laurens'
DANIEL = 'daniel'


def start_bots(os, bot1_name, bot2_name):
    print('start bots')

    bot1 = get_bot(bot1_name)
    bot2 = None
    if bot2_name is not None:
        bot2 = get_bot(bot2_name)

    print('bot1:', bot1.get_action())
    if bot2_name is not None:
        print('bot2:', bot2.get_action())

    while True:
        print('{}\'s next move: {}'.format(bot1_name, bot1.get_action()))
        print('{}\'s next move: {}'.format(bot2_name, bot2.get_action()))
        time.sleep(1)


def get_bot(bot_name):
    if bot_name == LAURENS:
        return Laurens()
    elif bot_name == DANIEL:
        return Daniel()
    else:
        raise Exception("Unexpected bot name: {}".format(bot_name))