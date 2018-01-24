import pygame
from pygame.math import Vector2
from pygame import Rect


class Destination:

    def __init__(self, size=None, position=None, color=None):
        self.size = size or (10, 10)
        self.position = position or Vector2()
        self.color = color or (0, 255, 0)

        self.body = Rect((0, 0), self.size)
        self.body.center = self.position

    def update(self):
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.body)


