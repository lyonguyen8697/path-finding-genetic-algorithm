import pygame
from pygame import Rect
from Population import Population
from Object import Object


class Environment:

    def __init__(self, rect=None):
        self.populations = []
        self.obstacles = []
        self.passages = []

        self.rect = rect

        self.__obstacle__ = None
        self.__drawing_obstacle__ = False
        self.__obstacle_start__ = None

    def update(self):
        for o in self.passages + self.populations + self.obstacles:
            o.update()

    def draw(self, screen):
        for o in self.passages + self.populations + self.obstacles:
            o.draw(screen)

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.start_draw_obstacle(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            self.draw_obstacle(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.end_draw_obstacle()

    def start_draw_obstacle(self, position):
        if self.__drawing_obstacle__:
            return
        self.__drawing_obstacle__ = True
        self.__obstacle_start__ = position

    def draw_obstacle(self, position):
        if not self.__drawing_obstacle__:
            return

        pos1 = self.__obstacle_start__
        pos2 = position

        width = abs(pos1[0] - pos2[0])
        height = abs(pos1[1] - pos2[1])

        left = pos1[0] - width if pos1[0] > pos2[0] else pos2[0] - width
        top = pos1[1] - height if pos1[1] > pos2[1] else pos2[1] - height

        if self.__obstacle__:
            self.remove_passage(self.__obstacle__)
        self.__obstacle__ = Object(size=(width, height), position=(left, top), pos_center=False, color=(244, 244, 244))
        self.add_passage(self.__obstacle__)

    def end_draw_obstacle(self):
        if not self.__drawing_obstacle__:
            return
        self.__drawing_obstacle__ = False
        self.__obstacle__.color = (0, 0, 0)
        self.add_obstacle(self.__obstacle__)
        self.__obstacle__ = None

    def add_population(self, population):
        if not isinstance(population, Population):
            raise TypeError()
        if population not in self.populations:
            population.environment = self
            self.populations.append(population)

    def add_obstacle(self, obstacle):
        if not isinstance(obstacle, Object):
            raise TypeError()
        if obstacle not in self.obstacles:
            self.obstacles.append(obstacle)

    def add_passage(self, passage):
        if not isinstance(passage, Object):
            raise TypeError()
        if passage not in self.passages:
            self.passages.append(passage)

    def remove(self, o):
        if isinstance(o, Population):
            if o in self.populations:
                self.populations.remove(o)
        elif isinstance(o, Object):
            if o in self.obstacles:
                self.obstacles.remove(o)
            elif o in self.passages:
                self.passages.remove(o)
        else:
            raise TypeError()

    def remove_population(self, population):
        if not isinstance(population, Population):
            raise TypeError()
        if population in self.populations:
            self.populations.remove(population)

    def remove_obstacle(self, obstacle):
        if not isinstance(obstacle, Object):
            raise TypeError()
        if obstacle in self.obstacles:
            self.obstacles.remove(obstacle)

    def remove_passage(self, passage):
        if not isinstance(passage, Object):
            raise TypeError()
        if passage in self.passages:
            self.passages.remove(passage)

    def __contains__(self, item):
        return item in self.populations + self.obstacles + self.passages

    def __len__(self):
        return len(self.populations) + len(self.obstacles) + len(self.passages)

    def __iter__(self):
        return (self.populations + self.obstacles + self.passages).__iter__()
