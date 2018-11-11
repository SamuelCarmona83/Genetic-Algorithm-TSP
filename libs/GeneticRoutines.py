from random import random, randint
from TSP import Route as Chromosome


#ruleta
def selection(pop):
    i = -1
    rand = random()
    while rand > 0:
        i += 1
        rand -= pop[i].chance
    return pop[i]


def mutation(population, rate):
    for chromosome in population:
        if random() < rate:
                r1 = randint(0, len(chromosome.genes) - 1)
                r2 = randint(0, len(chromosome.genes) - 1)
                chromosome.genes[r1], chromosome.genes[r2] = chromosome.genes[r2], chromosome.genes[r1]


def crossover(chromosome1, chromosome2):
    # que pasaria si no se cruzan? cual es el porcentaje?
    end = randint(0, len(chromosome1.genes))
    start = randint(0, end)
    section = chromosome1.genes[start:end] #seccion aleatoria de enteros?
    offspring_genes = list(gene if gene not in section else None for gene in chromosome2.genes)
    g = (x for x in section)
    for i, x in enumerate(offspring_genes):
        if x is None:
            offspring_genes[i] = next(g)
    offspring = Chromosome(offspring_genes, shuffled=True)

    return offspring
