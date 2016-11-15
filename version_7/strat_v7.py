from .hlt import *
from .networking import *
from .strategy import Strategy
from .plan import Plan
from .fast_expand import FastExpandStrategy
from .group import Group
from .manager import GameManager


class V7 (Strategy):
    GROUP_SIZE = 3
    GROUP_CUTOFF = 9

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.groups = [Group([], FastExpandStrategy(*args, **kwargs)) for a in range(int(V7.GROUP_CUTOFF / V7.GROUP_SIZE))]
        self.plan = Plan()

    def do_turn(self):

        # split into groups and fast expand
        if Strategy.owned_tiles <= V7.GROUP_CUTOFF:

            # check for new tiles to assign
            for tile in self.our_map_locations():
                has_g = False
                for group in self.groups:
                    if tile in group:
                        has_g = True
                        break

                if not has_g:
                    for group in self.groups:
                        if len(group) < V7.GROUP_SIZE:
                            group.append(tile)
                            break

            for group in self.groups:
                if len(group) > 0:
                    group.do_turn()

            return

        for here in self.our_map_locations():

            # check plan
            move = self.plan.pop(here, GameManager.turn_number)
            if move is not None:

                # safety check for overzealous planning
                if not (move == STILL and GameManager.game_map.getSite(here).strength > 200):
                    GameManager.plan_hits += 1
                    GameManager.send_move(here, move)
                    # skip everything else
                    continue

            all_us = True

            # make a list of neighboors that arent owned by us
            options = []
            for d in CARDINALS:
                if GameManager.game_map.getSite(here, d).owner != GameManager.ID:
                    all_us = False
                    options += [(GameManager.game_map.getSite(here, d), d)]

            # we have neighboors not owned by us, set plan to wait until big enough than grab it
            if not all_us:

                # find best value and direction
                d = STILL
                target = None
                for option in options:
                    if target is None or option[0].value() > target.value():
                        target = option[0]
                        d = option[1]

                # compare ours strength to the lowest
                our_site = GameManager.game_map.getSite(here)
                if our_site.strength > target.strength:

                    # we can take it immeditately
                    GameManager.send_move(here, d)
                    continue

                else:

                    # figure out how many turns to wait, wait that many, then take
                    if our_site.production > 0:
                        turn_delta = 1 + int ((target.strength - our_site.strength) / our_site.production)
                        for a in range(turn_delta - 1):
                            self.plan.insert(here, STILL, GameManager.turn_number + a + 1)
                        self.plan.insert(here, d, GameManager.turn_number + turn_delta + 1)

                        GameManager.send_move(here, STILL)
                        continue

                    else:

                        GameManager.send_move(here, d)
                        continue

            # if completely surrounded, wait until a certain size then move towards closest border
            else:
                # wait until size
                if GameManager.game_map.getSite(here).strength >= 30:

                    # find closest border
                    distances = [
                        self.get_distance_to_border(here, NORTH),
                        self.get_distance_to_border(here, EAST),
                        self.get_distance_to_border(here, SOUTH),
                        self.get_distance_to_border(here, WEST),
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
                    GameManager.send_move(here, dir)

                    # set planned moves
                    loc = here
                    for a in range(dist - 2):
                        loc = GameManager.game_map.getLocation(loc, dir)
                        self.plan.insert(loc, dir, GameManager.turn_number + a + 1)
