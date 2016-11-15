from .hlt import *

# able to insert moves we know we should do
class Plan:
    def __init__(self):
        self.moves = {}

    @staticmethod
    def _key_for_location(location, turn) -> str:
        return '%s,%s,%s' % (location.x, location.y, turn)

    # checks for move entry at location, and if it exists, pops it
    def pop(self, location, turn) -> int:
        key = Plan._key_for_location(location, turn)
        return self.moves.get(key, None)

    # insert a move
    def insert(self, location, direction, turn) -> None:
        key = Plan._key_for_location(location, turn)
        self.moves [key] = direction

    # insert a hesitant wait; if theres already a non-wait move saved, dont bother overriding
    def insert_wait_safely(self, location, turn) -> None:
        entry = self.pop(location, turn)

        if entry is None:
            self.insert(location, STILL, turn)
