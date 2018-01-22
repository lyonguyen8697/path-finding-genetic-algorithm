import sys, pygame
from pygame.math import Vector2
from Environment import Environment
from Population import Population
from Destination import Destination
from Obstacle import Obstacle

class Main:

    width = 1280
    height = 720

    backgroundColor = (95, 183, 229)

    objects = []
    texts = []

    def __init__(self):
        pygame.init()
        self.size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.time_step = 0

        self.objects.append(self.createEnvironment())

    def createEnvironment(self):
        environment = Environment()
        destination = Destination(size=(10, 100), position=Vector2(1200, 360))
        population1 = Population(destination=destination, size=20, position=Vector2(100, 360))
        population2 = Population(destination=destination, size=20, position=Vector2(100, 360), color=(255, 0, 0))
        population3 = Population(destination=destination, size=20, position=Vector2(100, 360), color=(166, 0, 45))
        population4 = Population(destination=destination, size=20, position=Vector2(100, 360), color=(50, 30, 168))
        obstacle1 = Obstacle(size=(10, 200), position=Vector2(640, 320))

        environment.add(population1)
        environment.add(population2)
        environment.add(population3)
        environment.add(population4)
        environment.add(destination)
        environment.add(obstacle1)

        return environment

    def createText(self, text, font="Comic San MS", size=30):
        font = pygame.font.SysFont(font, size)
        return font.render(text, False, (0, 0, 0))

    def renderGenerationNumber(self, screen, environment):
        generationNumber = environment.populations[0].generationNumber
        text = self.createText("Generation: %s" % generationNumber)
        screen.blit(text, (0, 0))

    def run(self):
        while True:
            dt = self.clock.tick(60)
            self.time_step += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                self.handle(event)

            self.update(dt / 1000)
            self.draw(self.screen)

    def draw(self, screen):
        screen.fill(self.backgroundColor)

        for o in self.objects:
            o.draw(screen)
            if isinstance(o, Environment):
                self.renderGenerationNumber(screen, o)

        pygame.display.flip()

    def update(self, dt):
        for o in self.objects:
            o.update()

    def handle(self, event):
        pass


if __name__ == "__main__":
    game =  Main()
    game.run()
