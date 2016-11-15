from .hlt import *
from .strategy import Strategy
from .plan import Plan
from .manager import GameManager


# finds best value neighboor and focuses all efforts on capturing that one first
class FastExpandStrategy(Strategy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.plan = Plan()
        self.target = None

    # evaluate and score a tile based on strength and production
    def get_value(self, game_map, location) -> float:
        s = game_map.getSite(location)
        return s.value()

    # finds best value target to capture next
    def find_target(self, group, game_map) -> None:

        # get all options
        options = []
        for tile in group:
            for d in CARDINALS:
                l = game_map.getLocation(tile, d)
                if game_map.getSite(l).owner != GameManager.ID:
                    options.append(l)

        # reduce to unique entries
        options = list(set(options))

        # find best
        target = None
        best_val = 0
        for option in options:
            v = self.get_value(game_map, option)
            if v > best_val:
                best_val = v
                target = option

        # sanity log check
        if target:
            self.target = target
            GameManager.log('Target is %s' % self.target)
        else:
            GameManager.log('WARNING: No target found :(')

    # returns direction to go to if at loc and wanting to head towards target, traversing only owned tiles
    def get_dir_to_target(self, loc) -> int:
        if self.target.x > loc.x and (GameManager.game_map.getSite(loc, EAST).owner == GameManager.ID or GameManager.game_map.getLocation(loc, EAST) == self.target):
            return EAST
        elif self.target.x < loc.x and (GameManager.game_map.getSite(loc, WEST).owner == GameManager.ID or GameManager.game_map.getLocation(loc, WEST) == self.target):
            return WEST
        elif self.target.y < loc.y and (GameManager.game_map.getSite(loc, NORTH).owner == GameManager.ID or GameManager.game_map.getLocation(loc, NORTH) == self.target):
            return NORTH
        elif self.target.y > loc.y and (GameManager.game_map.getSite(loc, SOUTH).owner == GameManager.ID or GameManager.game_map.getLocation(loc, SOUTH) == self.target):
            return SOUTH
        else:
            for d in CARDINALS:
                if GameManager.game_map.getSite(loc, d).owner == GameManager.ID:
                    return d

    # implement super try hard strat
    def do_turn(self, group) -> None:

        # make sure we have a target
        self.find_target(group, GameManager.game_map)

        # find total strength, production, and how many turns we (might) have to wait
        total_str = sum([GameManager.game_map.getSite(loc).strength for loc in group])
        total_prod = sum([GameManager.game_map.getSite(loc).production for loc in group])
        turns_to_wait = int((GameManager.game_map.getSite(self.target).strength - total_str) / total_prod)

        # iter all locations in group
        for loc in group:

            # sanity log
            GameManager.log('turn for %s' % loc)

            # check plan
            move = self.plan.pop(loc, GameManager.turn_number)
            if move is not None:

                # safety check for overzealous planning
                if not (move == STILL and GameManager.game_map.getSite(loc).strength > 200):
                    GameManager.plan_hits += 1
                    GameManager.send_move(loc, move)
                    # skip everything else
                    continue

            # move towards and capture
            if total_str > GameManager.game_map.getSite(self.target).strength:
                d = self.get_dir_to_target(loc)
                GameManager.send_move(loc, d)

            else:
                # plan waiting
                for a in range(turns_to_wait - 1):
                    GameManager.log('inserting planned move for turn %s' % (GameManager.turn_number + a + 1))
                    self.plan.insert(loc, STILL, GameManager.turn_number + a + 1)

                # plan movement afterwards
                moves = []
                loc_ = loc
                while (loc_ != self.target and len(moves) < 10):
                    d = self.get_dir_to_target(loc_)
                    moves += [(loc_, d)]
                    loc_ = GameManager.game_map.getLocation(loc_, d)

                # sanity log
                if len(moves) >= 10:
                    GameManager.log('WARNING: couldnt find path to target (cause this algo sucks you lazy piece of shit -.-)')

                # append movement
                for a in range(len(moves)):
                    self.plan.insert(moves[a][0], moves[a][1], GameManager.turn_number + turns_to_wait + a + 1)

                # if groups are 4, worst case is 4 moves to get to target, average is 3
                # therefor, we will append 2 rests at the end of every movement
                # average case is good enough to make a difference
                for a in range(2):
                    self.plan.insert_wait_safely(loc, GameManager.turn_number + turns_to_wait + a + 2)

                # current turns waiting
                GameManager.send_move(loc, STILL)
