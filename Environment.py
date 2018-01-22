from Population import Population
from Destination import Destination
from Obstacle import Obstacle


class Environment:

    def __init__(self):
        self.populations = []
        self.destinations = []
        self.obstacles = []

    def draw(self, screen):
        for o in self.populations + self.destinations + self.obstacles:
            o.draw(screen)

    def update(self):
        for o in self.populations + self.destinations + self.obstacles:
            o.update()

    def add(self, o):
        if isinstance(o, Population):
            o.environment = self
            self.populations.append(o)
        elif isinstance(o, Destination):
            self.destinations.append(o)
        elif isinstance(o, Obstacle):
            self.obstacles.append(o)
        else:
            raise TypeError()

    def remove(self, o):
        if isinstance(o, Population):
            self.populations.remove(o)
        elif isinstance(o, Destination):
            self.destinations.remove(o)
        elif isinstance(o, Obstacle):
            self.obstacles.remove(o)
        else:
            raise TypeError()

    def __contains__(self, item):
        return item in self.populations + self.destinations + self.obstacles

    def __len__(self):
        return len(self.populations) + len(self.destinations) + len(self.obstacles)

    def __iter__(self):
        return (self.populations + self.destinations + self.obstacles).__iter__()
