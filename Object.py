import pygame
from pygame.math import Vector2
from pygame import Rect


class Object:

    def __init__(self, size=None, position=None, color=None, pos_center=True):
        self.size = size or (10, 10)
        self.position = position or Vector2()
        self.color = color or (0, 0, 0)

        self.body = Rect(self.position, self.size)
        if pos_center:
            self.body.center = self.position

    def update(self):
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.body)