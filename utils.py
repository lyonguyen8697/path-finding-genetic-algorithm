import random


def random_vec2():
    return (random.random() * 2 - 1, random.random() * 2 - 1)


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

