from .networking import *
from .hlt import *


class Strategy():
    owned_tiles = 0

    def __init__(self, myID, log):
        self.myID = myID
        self.log = log
        log('Strategy initialized')

    # given a location and direction, gets distance to border
    def get_distance_to_border(self, game_map, start, direction):
        dist = 0
        pos = start
        while (game_map.getSite(pos).owner == self.myID and dist < game_map.width / 2.0):
            pos = game_map.getLocation(pos, direction)
            dist += 1
        return dist

    # generator of all map locations
    def map_locations(self, game_map):
        for y in range(game_map.height):
            for x in range(game_map.width):
                yield Location(x, y)

    # generator of map locations owned by us
    def our_map_locations(self, game_map):
        owned_tiles = 0
        for location in self.map_locations(game_map):
            if game_map.getSite(location).owner == self.myID:
                owned_tiles += 1
                yield location

        Strategy.owned_tiles = owned_tiles

    # do 1 turn
    def do_turn(self, game_map):
        raise NotImplemented()

