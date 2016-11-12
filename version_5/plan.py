
# able to insert moves we know we should do
class Plan():
    def __init__(self):
        self.moves = {}

    @staticmethod
    def _key_for_location(location, turn):
        return '%s,%s,%s' % (location.x, location.y, turn)

    # checks for move entry at location, andif it exists, pops it
    def pop(self, location, turn):
        key = Plan._key_for_location(location, turn)
        return self.moves.get(key, None)

    # insert a move
    def insert(self, location, direction, turn):
        key = Plan._key_for_location(location, turn)
        self.moves [key] = direction