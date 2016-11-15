from .networking import *
from .logger import Log
from .strat_v7 import V7
from .manager import GameManager


VERSION_NUM = 6

BOT_NAME = 'Lucas.v%s' % VERSION_NUM


def run():
    log = Log('%s__log__.txt' % BOT_NAME)
    my_id, game_map = getInit()

    GameManager.game_map = game_map
    GameManager.ID = my_id
    GameManager.log = log

    s = V7()

    sendInit(BOT_NAME)

    while True:
        GameManager.tick()
        s.do_turn()
        GameManager.tock()


