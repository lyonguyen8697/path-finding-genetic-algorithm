import random as rand
import time
import utils


class DNA:

    def __init__(self, genes_len=200, genes=None):
        self.genes_len = genes_len
        self.fitness = 0

        if not genes:
            self.random()
        else:
            self.genes = genes
            self.genes_len = len(genes)

    def random(self):
        self.genes = []
        for i in range(self.genes_len):
            self.genes.append(utils.random_vec2())

    def mate(self, other):
        pivot = rand.randrange(self.genes_len)

        child = self.genes[:self.genes_len] + other.genes[self.genes_len:]

        return DNA(genes=child)

    def mate_twins(self, other):
        pivot = rand.randrange(self.genes_len)

        child1 = self.genes[:self.genes_len] + other.genes[self.genes_len:]
        child2 = other.genes[:self.genes_len] + self.genes[self.genes_len:]

        return [DNA(genes=child1), DNA(genes=child2)]

    def mutate(self, mutation_rate):
        for i in range(self.genes_len):
            if rand.uniform(0, 1) < mutation_rate:
                self.genes[i] = utils.random_vec2()



