import pygame
from pygame import Surface
from pygame.math import Vector2


def create_body(radius, color):
    surface = Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(surface, (color[0], color[1], color[2], 155), (radius, radius), radius)
    pygame.draw.circle(surface, color, (radius, radius), radius, 4)
    return surface


class Circle:

    def __init__(self, radius=None, position=None, color=None, removable=True):
        self.radius = radius or 10
        self.position = position or Vector2()
        self.color = color or (192, 192, 192)
        self.removable = removable

        self.surface = create_body(self.radius, self.color)
        self.body = self.surface.get_rect()
        self.body.center = self.position

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.surface, self.body)