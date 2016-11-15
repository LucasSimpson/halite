from .hlt import Move
from .networking import getFrame, sendFrame


# hold globally available stuff
class GameManager:
    turn_number = -1
    moves = []
    game_map = None
    ID = -1
    log = None

    total_moves = 0
    plan_hits = 0

    @staticmethod
    def tick():
        GameManager.turn_number += 1
        GameManager.game_map = getFrame()
        GameManager.log('\nStarting turn %s' % GameManager.turn_number)
        GameManager.total_moves = 0
        GameManager.plan_hits = 0

    @staticmethod
    def tock():
        sendFrame(GameManager.moves)
        GameManager.moves = []
        GameManager.log('Finished turn %s: %s total moves, %s plan hits (%s)' % (GameManager.turn_number, GameManager.total_moves, GameManager.plan_hits, 100 * GameManager.plan_hits / GameManager.total_moves))

    @staticmethod
    def send_move(location, direction):
        GameManager.total_moves += 1
        GameManager.moves.append(Move(location, direction))

        # sanity log
        if direction is None:
            GameManager.log('CRITICAL: %s got move of None!' % location)
        else:
            GameManager.log('%s doing move %s' % (location, direction))



