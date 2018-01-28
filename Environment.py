import pygame
from pygame.math import Vector2
from Population import Population
from Rectangle import Rectangle
from Circle import Circle
import utils


class Environment:

    def __init__(self, rect=None):
        self.populations = []
        self.obstacles = []
        self.passages = []

        self.record = None

        self.paused = False

        self.rect = rect

        self.__obstacle__ = None
        self.__drawing_obstacle__ = False
        self.__obstacle_start__ = None

    def update(self):
        if self.paused:
            return
        for o in self.passages:
            o.update()
        for o in self.populations:
            o.update()
            self.update_record(o.record)
        for o in self.obstacles:
            o.update()

    def draw(self, screen):
        for o in self.passages + self.populations + self.obstacles:
            o.draw(screen)

        self.draw_distance_line(screen)

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.start_draw_obstacle(event.pos)
            elif event.button == 3:
                self.handle_right_mouse_button_clicked(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            self.draw_obstacle(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.end_draw_obstacle()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.paused = not self.paused
            elif event.key == pygame.K_F1:
                for population in self.populations:
                    population.reset()
            elif event.key == pygame.K_F2:
                for population in self.populations:
                    for i in range(population.age, population.lifetime - 1):
                        population.update()
            elif event.key == pygame.K_F3:
                for population in self.populations:
                    if population.size > 2:
                        population.size -= 1
            elif event.key == pygame.K_F4:
                for population in self.populations:
                    population.size += 1
            elif event.key == pygame.K_F5:
                for population in self.populations:
                    if population.mutation_rate > 0:
                        population.mutation_rate = round(population.mutation_rate - 0.001, 3)
            elif event.key == pygame.K_F6:
                for population in self.populations:
                    if population.mutation_rate < 1:
                        population.mutation_rate = round(population.mutation_rate + 0.001, 3)

    def update_record(self, record):
        if self.record:
            if record and record < self.record:
                self.record = record
        else:
            self.record = record

    def draw_distance_line(self, screen):
        fitness_creature = None
        min_distance = None
        des = None
        for pop in self.populations:
            for creature in pop.creatures:
                if creature.reached:
                    continue
                distance = creature.position.distance_squared_to(pop.destination.position)
                if not fitness_creature or distance < min_distance:
                    fitness_creature = creature
                    min_distance = distance
                    des = utils.round_vec2(pop.destination.position)

        if fitness_creature:
            center = fitness_creature.position
            pos = utils.calc_point_on_line(center, des, 16)
            pygame.draw.circle(screen, (244, 66, 66), utils.round_vec2(center), 16, 2)
            pygame.draw.line(screen, (244, 66, 66), pos, des, 2)

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
        self.__obstacle__ = Rectangle(size=(width, height), position=(left, top), pos_center=False, color=(244, 244, 244))
        self.add_passage(self.__obstacle__)

    def end_draw_obstacle(self):
        if not self.__drawing_obstacle__:
            return
        self.__drawing_obstacle__ = False

        if self.__obstacle__:
            if self.__obstacle__.size[0] >= 10 or self.__obstacle__.size[1] >= 10:
                obstacle = Rectangle(size=self.__obstacle__.size, position=self.__obstacle__.position, pos_center=False, color=(192, 192, 192))
                self.add_obstacle(obstacle)

            self.remove_passage(self.__obstacle__)
            self.__obstacle__ = None

    def cancel_draw_obstacle(self):
        self.__drawing_obstacle__ = False

        if self.__obstacle__:
            self.remove_passage(self.__obstacle__)
            self.__obstacle__ = None

    def remove_obstacle_at_position(self, position):
        for o in reversed(self.passages + self.obstacles):
            if o.removable and o.body.collidepoint(position):
                self.remove(o)
                return

    def handle_right_mouse_button_clicked(self, position):
        if self.__drawing_obstacle__:
            self.cancel_draw_obstacle()
        else:
            self.remove_obstacle_at_position(position)

    def add_population(self, population):
        if not isinstance(population, Population):
            raise TypeError()
        if population not in self.populations:
            population.environment = self
            self.populations.append(population)

    def add_obstacle(self, obstacle):
        if not (isinstance(obstacle, Rectangle) or isinstance(obstacle, Circle)):
            raise TypeError()
        if obstacle not in self.obstacles:
            self.obstacles.append(obstacle)

    def add_passage(self, passage):
        if not (isinstance(passage, Rectangle) or isinstance(passage, Circle)):
            raise TypeError()
        if passage not in self.passages:
            self.passages.append(passage)

    def remove(self, o):
        if isinstance(o, Population):
            if o in self.populations:
                self.populations.remove(o)
        elif isinstance(o, Rectangle) or isinstance(o, Circle):
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
        if not (isinstance(obstacle, Rectangle) or isinstance(obstacle, Circle)):
            raise TypeError()
        if obstacle in self.obstacles:
            self.obstacles.remove(obstacle)

    def remove_passage(self, passage):
        if not (isinstance(passage, Rectangle) or isinstance(passage, Circle)):
            raise TypeError()
        if passage in self.passages:
            self.passages.remove(passage)

    def __contains__(self, item):
        return item in self.populations + self.obstacles + self.passages

    def __len__(self):
        return len(self.populations) + len(self.obstacles) + len(self.passages)

    def __iter__(self):
        return (self.populations + self.obstacles + self.passages).__iter__()
