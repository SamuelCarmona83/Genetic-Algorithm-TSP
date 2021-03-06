from libs.GeneticRoutines import selection, mutation, crossover
import time
from random import random, randint
import math 


class GeneticAlgorithm:
    def __init__(self, size, mutation_rate=0.01, ptype=None, args=tuple()):
        assert ptype is not None, 'Population type cannot be None'
        assert type(args) == tuple, 'Arguments must be a tuple instead of ' + str(type(args))
        self._population = [ptype(*args) for _ in range(size)]
        self._mutation_rate = mutation_rate
        self._generation = 0
        self._fittest = self._population[0]
        self.evaluation()

    def individuals(self):
        for chromosome in self._population:
            yield chromosome

    def evaluation(self):
        fitness_sum = sum(chromosome.fitness for chromosome in self._population)
        for chromosome in self._population:
            chromosome.chance = chromosome.fitness / fitness_sum # Importante 

    def best(self):
        return max(self._population, key=lambda k: k.fitness)
        #key - key function where each argument is passed, and comparison is performed based on its return value

    @property
    def alltime_best(self):
        return self._fittest

    @property
    def generation(self):
        return self._generation

    def next_generation(self):
        new_population = []
        #for _ in range(len(self._population)):
        y = 0
        while y < len(self._population):
            x = random()
            if x < 0.90: # Probabilidad de cruce
                chromosome1 = selection(self._population)
                chromosome2 = selection(self._population)
                new_population.append(crossover(chromosome1, chromosome2))
                mutation(new_population, self._mutation_rate)
                y = y + 1 
        self._population = new_population
        self.evaluation()

    def run(self, seconds=5, reps=None):
        if reps is not None:
            assert isinstance(reps, int), 'Argument `reps` must be of integer type'
            for _ in range(reps - 1):
                pretender = self.best()
                if pretender.fitness > self._fittest.raw_fitness:
                    self._fittest = pretender.copy()

                self._generation += 1
                self.next_generation()
            pretender = self.best()
            if pretender.fitness > self._fittest.raw_fitness:
                self._fittest = pretender.copy()
            self._generation += 1
        else:
            t0 = time.time()
            count = 0
            M1 = 0
            M2 = 0
            while True:
                pretender = self.best()
                if pretender.fitness > self._fittest.raw_fitness:
                    self._fittest = pretender.copy()
                    M1 = (math.fabs(pretender.fitness - self._fittest.raw_fitness)/self._fittest.raw_fitness)
                    #count = 0
                #elif pretender.fitness == self._fittest.raw_fitness:
                    #count =+ 1
                self._generation += 1
                M2 = (math.fabs(pretender.fitness - self._fittest.raw_fitness)/self._fittest.raw_fitness)
                #or math.fabs(pretender.fitness - self._fittest.raw_fitness) > 0
                #time.time() - t0 >= seconds or
                #or (math.fabs(( M1 - M2 ))) < 0.015 and M1 != M2
                if time.time() - t0 >= seconds  : #condicion de parada
                    print("Ajuste :",(math.fabs(pretender.fitness - self._fittest.raw_fitness)/self._fittest.raw_fitness))
                    print ("time to converge: ",time.time() - t0)
                    break

                self.next_generation()
