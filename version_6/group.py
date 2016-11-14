

# defines a group of locations
class Group:
    group_counter = 0

    def __init__(self, locations, strategy):
        self.locations = locations
        self.strategy = strategy
        self.id = Group.group_counter
        Group.group_counter += 1

    def __str__(self):
        return 'Group(%s)' % self.id

    def __iter__(self):
        self.iter_count = -1
        return self

    def __next__(self):
        self.iter_count += 1

        if self.iter_count == len(self.locations):
            raise StopIteration

        return self.locations[self.iter_count]

    def __len__(self):
        return len(self.locations)

    def set_locations(self, locations):
        self.locations = locations

    def append(self, location):
        self.locations.append(location)

    def do_turn(self, game_map):
        return self.strategy.do_turn(self, game_map)

