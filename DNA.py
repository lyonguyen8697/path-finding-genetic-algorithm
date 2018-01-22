import random as rand
import time
import utils


class DNA:

    def __init__(self, genesLen=200, genes=None):
        self.genesLen = genesLen
        self.fitness = 0

        if not genes:
            self.random()
        else:
            self.genes = genes
            self.genesLen = len(genes)

    def random(self):
        self.genes = []
        for i in range(self.genesLen):
            self.genes.append(utils.randomVec2())

    def mate(self, other):
        pivot = rand.randrange(self.genesLen)

        child = self.genes[:self.genesLen] + other.genes[self.genesLen:]

        return DNA(genes=child)

    def mutate(self, mutationRate):
        for i in range(self.genesLen):
            if rand.uniform(0, 1) < mutationRate:
                self.genes[i] = utils.randomVec2()

