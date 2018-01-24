import sys, pygame
from pygame.math import Vector2
from pygame import Rect
from Environment import Environment
from Population import Population
from Object import Object

class Main:

    width = 1280
    height = 720

    background_color = (67, 209, 216)

    objects = []
    texts = []

    def __init__(self):
        pygame.init()
        self.size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.time_step = 0

        self.objects.append(self.create_environment())

    def create_environment(self):
        environment = Environment(rect=Rect((0, 0), (self.width, self.height)))
        destination = Object(size=(10, 100), position=Vector2(1200, 360), color=(0, 255, 0))
        population1 = Population(destination=destination, size=20, position=Vector2(100, 360))
        population2 = Population(destination=destination, size=20, position=Vector2(100, 360), color=(238, 244, 66))
        population3 = Population(destination=destination, size=20, position=Vector2(100, 360), color=(65, 244, 145))
        population4 = Population(destination=destination, size=20, position=Vector2(100, 360), color=(238, 65, 244))
        obstacle1 = Object(size=(10, 200), position=Vector2(640, 200))
        obstacle2 = Object(size=(10, 200), position=Vector2(640, 520))

        environment.add_population(population1)
        environment.add_population(population2)
        environment.add_population(population3)
        environment.add_population(population4)
        environment.add_obstacle(destination)
        environment.add_obstacle(obstacle1)
        environment.add_obstacle(obstacle2)

        return environment

    def create_text(self, text, font="Comic San MS", size=30):
        font = pygame.font.SysFont(font, size)
        return font.render(text, True, (0, 0, 0))

    def render_generation_number(self, screen, environment):
        generation_number = environment.populations[0].generation_number
        text = self.create_text("Generation: %s" % generation_number)
        screen.blit(text, (10, 10))

    def run(self):
        while True:
            dt = self.clock.tick(60)
            self.time_step += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                self.handle(event)

            self.update(self.screen, dt / 1000)
            self.draw(self.screen)

    def update(self, screen, dt):
        for o in self.objects:
            o.update()

    def draw(self, screen):
        screen.fill(self.background_color)

        for o in self.objects:
            o.draw(screen)
            if isinstance(o, Environment):
                self.render_generation_number(screen, o)

        pygame.display.flip()

    def handle(self, event):
        for o in self.objects:
            o.handle(event)


if __name__ == "__main__":
    game =  Main()
    game.run()
