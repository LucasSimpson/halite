from .hlt import *
from .strategy import Strategy
from .plan import Plan


# finds best value neighboor and focuses all efforts on capturing that one first
class FastExpandStrategy(Strategy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.plan = Plan()
        self.target = None

    # evaluate and score a tile based on strength and production
    def get_value(self, game_map, location):
        s = game_map.getSite(location)
        return s.value()

    # finds best value target to capture next
    def find_target(self, group, game_map):

        # get all options
        options = []
        for tile in group:
            for d in CARDINALS:
                l = game_map.getLocation(tile, d)
                if game_map.getSite(l).owner != self.myID:
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

        if target:
            self.target = target
            self.log('Target is %s' % self.target)
        else:
            self.log('No target found :(')

    # implement super try hard strat
    def do_turn(self, group, game_map):

        # make sure we have a target
       # if not self.target or game_map.getSite(self.target).owner == self.myID:
        self.find_target(group, game_map)

        # find total strength
        total_str = sum([game_map.getSite(loc).strength for loc in group])

        moves = []

        # move towards and capture
        if total_str > game_map.getSite(self.target).strength:

            for loc in group:

                if self.target.x > loc.x and (game_map.getSite(loc, EAST).owner == self.myID or game_map.getLocation(loc, EAST) == self.target):
                    moves.append(Move(loc, EAST))
                    self.log('%s doing move %s' % (loc, EAST))
                elif self.target.x < loc.x and (game_map.getSite(loc, WEST).owner == self.myID or game_map.getLocation(loc, WEST) == self.target):
                    moves.append(Move(loc, WEST))
                    self.log('%s doing move %s' % (loc, WEST))

                elif self.target.y < loc.y and (game_map.getSite(loc, NORTH).owner == self.myID or game_map.getLocation(loc, NORTH) == self.target):
                    moves.append(Move(loc, NORTH))
                    self.log('%s doing move %s' % (loc, NORTH))
                elif self.target.y > loc.y and (game_map.getSite(loc, SOUTH).owner == self.myID or game_map.getLocation(loc, SOUTH) == self.target):
                    moves.append(Move(loc, SOUTH))
                    self.log('%s doing move %s' % (loc, SOUTH))

                else:
                    for d in CARDINALS:
                        if game_map.getSite(loc, d).owner == self.myID:
                            moves.append (Move(loc, d))
                            self.log('%s doing move %s' % (loc, d))

        else:
            # wait
            for loc in group:
                moves.append(Move(loc, STILL))

        return moves