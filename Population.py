import random as rand
from pygame.math import Vector2
from Creature import Creature
import utils


class Population:

    def __init__(self, destination, size=20, mutation_rate=0.01 , lifetime=300, position=None, velocity=None, color=None):
        self.destination = destination
        self.size = size
        self.mutation_rate = mutation_rate
        self.lifetime = lifetime
        self.generation_number = 1
        self.age = 0
        self.color = color or (0, 0, 255)

        self.position = position or Vector2()
        self.velocity = velocity or Vector2()

        self.creatures = []
        self.fill()

    def fill(self):
        while len(self.creatures) < self.size:
            pos = Vector2(self.position)
            vel = Vector2(self.velocity)
            creature = Creature(lifetime=self.lifetime, position=pos, velocity=vel, color=self.color)
            self.creatures.append(creature)

    def draw(self, screen):
        for creature in self.creatures:
            creature.draw(screen)

    def update(self):
        for creature in self.creatures:
            creature.update()
            self.check_collision(creature)

        self.age += 1
        if self.age >= self.lifetime:
            self.generate()
            self.age = 0
        # if self.age >= self.lifetime or all(creature.stuck or creature.reached for creature in self.creatures):
        #     self.generate()
        #     self.age = 0

    def check_collision(self, creature):
        if creature.body.colliderect(self.destination.body):
            creature.reached = True
        elif creature.body.collidelist([obstacle.body for obstacle in self.environment.obstacles]) != -1 \
                or (self.environment.rect and not self.environment.rect.contains(creature.body)):
            creature.stuck = True

    def generate(self):
        self.calc_fitness()
        self.mate()
        self.mutate()
        self.generation_number += 1

    def mate(self):
        new_population = []
        count = 0
        while count < self.size:
            parent1 = utils.choice_distribution(self.creatures, lambda x: x.dna.fitness)
            parent2 = utils.choice_distribution(self.creatures, lambda x: x.dna.fitness, recalc=False)

            while parent1 == parent2:
                parent2 = utils.choice_distribution(self.creatures, lambda x: x.dna.fitness, recalc=False)

            child = parent1.mate(parent2, self.position, self.velocity)
            new_population.append(child)
            count += 1

        self.creatures = new_population

    def mutate(self):
        for creature in self.creatures:
            creature.mutate(self.mutation_rate)

    def calc_fitness(self):
        for creature in self.creatures:
            creature.calc_fitness(self.destination.position)
