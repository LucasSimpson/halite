from .networking import *
from .hlt import *
from .manager import GameManager


class Strategy():
    owned_tiles = 0

    def __init__(self):
        GameManager.log('Strategy initialized')

    # given a location and direction, gets distance to border
    def get_distance_to_border(self, start, direction):
        dist = 0
        pos = start
        while GameManager.game_map.getSite(pos).owner == GameManager.ID and dist < GameManager.game_map.width / 2.0:
            pos = GameManager.game_map.getLocation(pos, direction)
            dist += 1
        return dist

    # generator of all map locations
    def map_locations(self):
        for y in range(GameManager.game_map.height):
            for x in range(GameManager.game_map.width):
                yield Location(x, y)

    # generator of map locations owned by us
    def our_map_locations(self):
        owned_tiles = 0
        for location in self.map_locations():
            if GameManager.game_map.getSite(location).owner == GameManager.ID:
                owned_tiles += 1
                yield location

        Strategy.owned_tiles = owned_tiles

    # do 1 turn
    def do_turn(self):
        raise NotImplemented()

