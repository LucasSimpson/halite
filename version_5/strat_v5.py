from .hlt import *
from .networking import *
from .strategy import Strategy

from .plan import Plan

class V5 (Strategy):
    turn_count = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.plan = Plan()

    def do_turn(self, game_map):
        V5.turn_count += 1
        total_moves = 0
        hits = 0
        self.log('doing turn %s' % self.turn_count)

        moves = []

        for here in self.our_map_locations(game_map):
            total_moves += 1

            # check plan
            move = self.plan.pop(here, V5.turn_count)
            if move is not None:
                hits += 1
                moves += [Move(here, move)]
                # skip everything else
                continue

            allUs = True
            moved = False


            # make a list of neighboors that arent owned by us
            options = []
            for d in CARDINALS:
                if game_map.getSite(here, d).owner != self.myID:
                    allUs = False
                    options += [(game_map.getSite(here, d), d)]

            # we have neighboors not owned by us, set plan to wait until big enough than grab it
            if not allUs:

                # find lowest strength and direction its in
                lowest_strength = 256
                d = STILL
                for option in options:
                    if option[0].strength < lowest_strength:
                        lowest_strength = option[0].strength
                        d = option[1]

                # compare ours strength to the lowest
                our_site = game_map.getSite(here)
                if our_site.strength > lowest_strength:

                    # we can take it immeditately
                    moves.append(Move(here, d))
                    continue

                else:

                    # figure out how many turns to wait, wait that many, then take
                    if our_site.production > 0:
                        turn_delta = 1 + int ((lowest_strength - our_site.strength) / float(our_site.production))
                        for a in range(turn_delta-1):
                            self.plan.insert(here, STILL, V5.turn_count + a + 1)
                        self.plan.insert(here, d, V5.turn_count + turn_delta + 1)

                        moves.append(Move(here, STILL))
                        continue
                    else:
                        moves.append(Move(here, d))
                        continue


            # if completely surrounded, wait until a certain size then move towards closest border
            if allUs:
                # wait until size
                if game_map.getSite(here).strength >= 30:

                    # find closest border
                    distances = [
                        self.get_distance_to_border(game_map, here, NORTH),
                        self.get_distance_to_border(game_map, here, EAST),
                        self.get_distance_to_border(game_map, here, SOUTH),
                        self.get_distance_to_border(game_map, here, WEST),
                    ]
                    dir_index = 0
                    dist = distances[0]
                    for a in [1, 2, 3]:
                        if distances[a] < dist:
                            dist = distances[a]
                            dir_index = a

                    # move towards closest border
                    dir = [NORTH, EAST, SOUTH, WEST]
                    dir = dir[dir_index]
                    moves.append(Move(here, dir))

                    # set planned moves
                    loc = here
                    for a in range(dist - 1):
                        loc = game_map.getLocation(loc, dir)
                        self.plan.insert(loc, dir, V5.turn_count + a + 1)

        self.log('Turn %s, total=%s, hits=%s (%s)' % (V5.turn_count, total_moves, hits, 100.0*hits/total_moves))

        sendFrame(moves)
