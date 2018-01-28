import pygame
from pygame import Surface
from pygame.math import Vector2
from pygame import Rect


def create_body(size, color):
    surface = Surface(size, pygame.SRCALPHA)
    surface.fill((color[0], color[1], color[2], 155))
    pygame.draw.rect(surface, color, Rect((0, 0), (size[0] - 1, size[1] - 1)), 4)
    return surface


class Rectangle:

    def __init__(self, size=None, position=None, color=None, pos_center=True, removable=True):
        self.size = size or (10, 10)
        self.position = position or Vector2()
        self.color = color or (192, 192, 192)
        self.pos_center = pos_center
        self.removable = removable

        self.surface = create_body(self.size, self.color)
        self.body = self.surface.get_rect()
        if self.pos_center:
            self.body.center = self.position
        else:
            self.body.topleft = self.position

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.surface, self.body)