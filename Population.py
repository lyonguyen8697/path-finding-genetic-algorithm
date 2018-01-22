import random as rand
from pygame.math import Vector2
from Creature import Creature


class Population:

    def __init__(self, destination, size=20, mutationRate=0.005 , lifetime=200, position=None, velocity=None, color=None):
        self.destination = destination
        self.size = size
        self.mutationRate = mutationRate
        self.lifetime = lifetime
        self.generationNumber = 1
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
            self.creatures.append(Creature(lifetime=self.lifetime, position=pos, velocity=vel, color=self.color))

    def draw(self, screen):
        for creature in self.creatures:
            creature.draw(screen)

    def update(self):
        for creature in self.creatures:
            creature.update()
            self.checkCollision(creature)

        self.age += 1
        if self.age >= self.lifetime:
            self.generate()
            self.age = 0

    def checkCollision(self, creature):
        if creature.body.colliderect(self.destination.body):
            creature.reached = True
            return
        if creature.body.collidelist([obstacle.body for obstacle in self.environment.obstacles]) != -1:
            creature.stuck = True

    def generate(self):
        self.calcFitness()
        self.mate()
        self.mutate()
        self.generationNumber += 1

    def mate(self):
        newPopulation = []
        count = 0
        self.calcMatingRate()
        while count < self.size:
            parent1 = self.selectOne()
            parent2 = self.selectOne()

            while parent1 == parent2:
                parent2 = self.selectOne()

            child = parent1.mate(parent2, self.position, self.velocity)
            newPopulation.append(child)
            count += 1

        self.creatures = newPopulation

    def mutate(self):
        for creature in self.creatures:
            creature.mutate(self.mutationRate)

    def calcFitness(self):
        for creature in self.creatures:
            creature.calcFitness(self.destination.position)

    def calcMatingRate(self):
        total = sum(creature.dna.fitness for creature in self.creatures)
        for creature in self.creatures:
            creature.matingRate = creature.dna.fitness / total

    def selectOne(self):
        r = rand.uniform(0, 1)
        s = 0
        for creature in self.creatures:
            s += creature.matingRate
            if s >= r:
                return creature
        return creature

