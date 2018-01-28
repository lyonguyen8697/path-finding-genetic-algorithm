import sys, os, pygame
from pygame.math import Vector2
from pygame import Rect
from Environment import Environment
from Population import Population
from Rectangle import Rectangle
from Circle import Circle

os.environ['SDL_VIDEO_CENTERED'] = '1'


class Main:

    width = 1280
    height = 720

    fps = 60

    background_color = (255, 255, 255)

    objects = []
    texts = []

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Path finding genetic algorithm")
        pygame.key.set_repeat(500, 100)

        self.size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.time_step = 0

        self.objects.append(self.create_environment())

    def create_environment(self):
        environment = Environment(rect=Rect((0, 0), (self.width, self.height)))
        origin = Circle(radius=20, position=Vector2(80, 360), color=(128, 255, 255), removable=False)
        destination = Rectangle(size=(50, 50), position=Vector2(1200, 360), color=(102, 255, 102), removable=False)
        population1 = Population(destination=destination, size=20, position=Vector2(100, 360))
        population2 = Population(destination=destination, size=20, position=Vector2(100, 360), color=(204, 102, 255))
        population3 = Population(destination=destination, size=20, position=Vector2(100, 360), color=(102, 255, 153))
        population4 = Population(destination=destination, size=20, position=Vector2(100, 360), color=(255, 153, 255))
        obstacle1 = Rectangle(size=(20, 400), position=Vector2(425, 200))
        obstacle2 = Rectangle(size=(20, 400), position=Vector2(850, 520))

        environment.add_population(population1)
        environment.add_population(population2)
        environment.add_population(population3)
        environment.add_population(population4)
        environment.add_passage(origin)
        environment.add_obstacle(destination)
        # environment.add_obstacle(obstacle1)
        # environment.add_obstacle(obstacle2)

        return environment

    def create_text(self, text, font="Comic San MS", size=25):
        font = pygame.font.SysFont(font, size)
        return font.render(text, True, (0, 0, 0))

    def render_info(self, screen, environment):
        population = environment.populations[0]

        generation_number = population.generation_number
        text = self.create_text("Generation: %d" % generation_number)
        screen.blit(text, (5, 5))

        step_number = population.age
        text = self.create_text("Step: %d" % step_number)
        screen.blit(text, (5, 25))

        size = population.size
        text = self.create_text("Size: %d (per population)" % size)
        screen.blit(text, (5, 45))

        mutation_rate = population.mutation_rate
        text = self.create_text("Mutation: %0.1f %%" % (mutation_rate * 100))
        screen.blit(text, (5, 65))

        reached = sum([len([c for c in population.creatures if c.reached]) for population in environment.populations])
        text = self.create_text("Reached: %d" % reached)
        screen.blit(text, (5, 85))

        record = environment.record
        text = self.create_text("Record (step): %s" % record)
        screen.blit(text, (5, 105))

        fps = round(self.clock.get_fps())
        text = self.create_text("FPS: %d" % fps, size=20)
        screen.blit(text, (1225, 5))

    def run(self):
        while True:
            dt = self.clock.tick(self.fps)
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
                self.render_info(screen, o)

        pygame.display.flip()

    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_MINUS and self.fps > 2:
                self.fps -= 2
            elif event.key == pygame.K_EQUALS and self.fps < self.clock.get_fps() + 10:
                self.fps += 2

        for o in self.objects:
            o.handle(event)


if __name__ == "__main__":
    game = Main()
    game.run()
