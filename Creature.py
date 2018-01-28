import pygame
from pygame import gfxdraw
from pygame.math import Vector2
from pygame import Surface
from DNA import DNA
import utils


def create_body(color):
    original_image = Surface((16, 16), pygame.SRCALPHA)
    gfxdraw.aatrigon(original_image, 8, 0, 2, 16, 14, 16, color)
    gfxdraw.filled_trigon(original_image, 8, 0, 2, 16, 14, 16, color)
    return original_image


class Creature:

    def __init__(self, dna=None, lifetime=200, position=None, velocity=None, color=None):
        self.dna = dna or DNA(genes_len=lifetime)
        self.lifetime = lifetime
        self.step = 0
        self.color = color

        self.position = position or Vector2()
        self.velocity = velocity or Vector2()
        self.acceleration = Vector2()
        self.reached = False
        self.stuck = False

        self.original_image = create_body(color)
        self.image = self.original_image
        self.body = self.original_image.get_rect(center=self.position)
        self.body.size = (10, 10)

    def update(self):
        if self.reached or self.stuck:
            return
        if self.step < self.lifetime:
            self.move(self.dna.genes[self.step])
            self.step += 1

        self.velocity += self.acceleration
        self.position += utils.round_vec2(self.velocity)
        self.acceleration = Vector2()

        self.image = pygame.transform.rotate(self.original_image, self.velocity.angle_to((0, -1)))
        self.body.center = self.position

    def draw(self, screen):
        screen.blit(self.image, self.body)

    def move(self, force):
        self.acceleration += force

    def mate(self, other, position=None, velocity=None):
        dna = self.dna.mate(other.dna)
        pos = Vector2(position) if position else Vector2()
        vel = Vector2(velocity) if velocity else None
        return Creature(dna=dna, lifetime=self.lifetime, position=pos, velocity=vel, color=self.color)

    def mate_twins(self, other, position=None, velocity=None):
        dna = self.dna.mate_twins(other.dna)
        pos1, pos2 = Vector2(position), Vector2(position) if position else Vector2()
        vel1, vel2 = Vector2(velocity), Vector2(velocity) if velocity else None
        return [Creature(dna[0], self.lifetime, pos1, vel1, self.color), Creature(dna[1], self.lifetime, pos2, vel2, self.color)]

    def mutate(self, mutation_rate):
        self.dna.mutate(mutation_rate)

    def calc_fitness(self, destination):
        if self.reached:
            self.dna.fitness = (pow(self.lifetime, 2) / pow(self.step, 2)) * 10
            return

        distance = self.position.distance_squared_to(destination)
        self.dna.fitness = 1000000 / distance

        if self.stuck:
            self.dna.fitness /= 10
