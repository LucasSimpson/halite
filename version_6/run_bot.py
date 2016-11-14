from .networking import *
from .logger import Log
from .strat_v6 import V6

VERSION_NUM = 6

BOT_NAME = 'Lucas.v%s' % VERSION_NUM


def run():

    my_id, game_map = getInit()

    log = Log('%s__log__.txt' % BOT_NAME)
    s = V6(my_id, log)

    sendInit(BOT_NAME)

    while True:
        game_map = getFrame()
        s.do_turn(game_map)

