import random
from pygame.math import Vector2

def random_vec2():
    return (random.random() * 2 - 1, random.random() * 2 - 1)


def round_vec2(vector):
    return (round(vector[0]), round(vector[1]))


def choice_distribution(data, key, recalc=True):
    if recalc:
        total = sum(key(d) for d in data)
        for d in data:
            d.__prob = key(d) / total

    r = random.uniform(0, 1)
    s = 0
    for d in data:
        s += d.__prob
        if s >= r:
            return d
    return d


def calc_point_on_line(start, end, distance):
    start = Vector2(start)
    end = Vector2(end)
    u = (end.elementwise() - start.elementwise()).normalize()
    return start.elementwise() + distance * u.elementwise()

