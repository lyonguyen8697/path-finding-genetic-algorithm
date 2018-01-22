import pygame
from pygame.math import Vector2
from pygame import Rect
from DNA import DNA
import utils
import math


class Creature:

    def __init__(self, dna=None, lifetime=200, position=None, velocity=None, color=None):
        self.dna = dna or DNA(genesLen=lifetime)
        self.lifetime = lifetime
        self.step = 0

        self.position = position or Vector2()
        self.velocity = velocity or Vector2()
        self.acceleration = Vector2()
        self.reached = False
        self.stuck = False

        self.body = Rect((0, 0, 10, 10))
        self.body.center = self.position
        self.color = color or (0, 0, 255)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.body)

    def update(self):
        if self.reached or self.stuck:
            return
        if self.step < self.lifetime:
            self.move(self.dna.genes[self.step])
            self.step += 1

        self.velocity += self.acceleration
        self.position += self.velocity
        self.acceleration = Vector2()

        self.body.center = self.position

    def move(self, force):
        self.acceleration += force

    def mate(self, other, position=None, velocity=None):
        dna = self.dna.mate(other.dna)
        pos = Vector2(position) if position else Vector2()
        vel = Vector2(velocity) if velocity else None
        return Creature(dna=dna, lifetime=self.lifetime, position=pos, velocity=vel, color=self.color)

    def mutate(self, mutateRate):
        self.dna.mutate(mutateRate)

    def calcFitness(self, destination):
        if self.reached:
            self.dna.fitness = (pow(self.lifetime, 2) / pow(self.step, 2)) * 10
            return

        distance = self.position.distance_squared_to(destination)
        self.dna.fitness = 1000000 / distance

        if self.stuck:
            self.dna.fitness /= 10




