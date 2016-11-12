from .hlt import *
from .strategy import Strategy


class V4 (Strategy):
    turn_count = 0

    def do_turn(self, game_map):
        V4.turn_count += 1
        self.log('doing turn %s' % self.turn_count)

        moves = []

        for here in self.our_map_locations(game_map):

            self.log('calculating move for %s' % here)

            allUs = True
            moved = False

            # for computation resource reasons, we only do total calculations for some of the tiles
            if Strategy.owned_tiles > 0 and random.random() <= 500.0 / (Strategy.owned_tiles ** 1.2):

                for d in CARDINALS:
                    # check if there's a cell not owned by us beside
                    if game_map.getSite(here, d).owner != self.myID:
                        allUs = False

                        # check to see if we can take it
                        if game_map.getSite(here, d).strength < game_map.getSite(here).strength:
                            # if we can take it, set move
                            moves.append(Move(here, d))
                            moved = True
                            break

                # if completely surrounded, wait until a certain size then move towards closest border
                if allUs:
                    # wait until size
                    if game_map.getSite(here).strength >= 40:

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
                        moves.append(Move(here, dir[dir_index]))

            else:
                # move randomly :(
                # bias towards being still
                if random.random() <= 0.8:
                    moves.append(Move(here, STILL))
                else:
                    moves.append(Move(here, [NORTH, EAST, SOUTH, WEST][int(random.random() * 4)]))

        V4.send_moves(moves)
