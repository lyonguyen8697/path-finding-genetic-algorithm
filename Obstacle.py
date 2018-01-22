import pygame
from pygame.math import Vector2
from pygame import Rect


class Obstacle:

    def __init__(self, size=None, position=None, color=None):
        self.size = size or (10, 100)
        self.position = position or Vector2()

        self.color = color or (255, 255, 255)

        self.body = Rect((0, 0), self.size)
        self.body.center = self.position

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.body)

    def update(self):
        pass
