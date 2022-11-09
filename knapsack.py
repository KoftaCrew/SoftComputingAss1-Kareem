# Kareem Mohamed Morsy Ismail, ID: 20190386, Group: CS-S3, Program: CS
# David Emad Philip Ata-Allah, ID: 20190191, Group: CS-S3, Program: CS

import random


ITERATIONS = 1000
POPULATION_SIZE = 100
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.7


def inputNonEmpty():
    while True:
        s = input()
        if s != "":
            return s


def calculateFitness(individual, items):
    value = 0
    for i in range(len(individual)):
        if individual[i] == 1:
            value += items[i][1]
    return value


def calculateWeight(individual, items):
    weight = 0
    for i in range(len(individual)):
        if individual[i] == 1:
            weight += items[i][0]
    return weight


def initializePopulation(items, max_weight, population_size):
    population = []
    while len(population) < population_size:
        individual = [random.randint(0, 1) for _ in range(len(items))]
        if calculateWeight(individual, items) <= max_weight:
            population.append(individual)
    return population


def selection(population, fitness):
    # Sort the population by fitness
    population, fitness = zip(
        *sorted(zip(population, fitness), key=lambda x: x[1])
    )

    # Generate cumulative array
    cumulative = [1]
    for i in range(2, len(population) + 1):
        cumulative.append(cumulative[-1] + i)

    # Select two random numbers
    r1 = random.randint(1, cumulative[-1])
    r2 = random.randint(1, cumulative[-1])

    # Find the index
    def indexFromCumulative(x, cumulative):
        l = 0
        r = len(cumulative) - 1
        while l < r:
            m = (l + r) // 2
            if cumulative[m] < x:
                l = m + 1
            else:
                r = m
        return l

    i1 = indexFromCumulative(r1, cumulative)
    i2 = indexFromCumulative(r2, cumulative)

    return population[i1], population[i2]


def crossover(parent1, parent2):
    # If the crossover rate is not met, return the parents
    if random.random() > CROSSOVER_RATE:
        return parent1, parent2

    # Find the crossover point
    crossover_point = random.randint(1, len(parent1) - 1)

    # Create the children
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]

    return child1, child2


def mutate(individual):
    for i in range(len(individual)):
        if random.random() < MUTATION_RATE:
            individual[i] = 1 - individual[i]
    return individual


def doWork(t):
    # Read in the data
    max_weight = int(inputNonEmpty())
    items_num = int(inputNonEmpty())
    items = [inputNonEmpty().split() for _ in range(items_num)]
    items = [(int(i[0]), int(i[1])) for i in items]

    population = initializePopulation(items, max_weight, POPULATION_SIZE)

    for _ in range(ITERATIONS):
        # Calculate the fitness of each individual
        fitness = [calculateFitness(i, items) for i in population]

        new_population = []

        while len(new_population) < POPULATION_SIZE:
            # Selection
            parent1, parent2 = selection(population, fitness)

            # Crossover
            child1, child2 = crossover(parent1, parent2)

            # Mutation
            child1 = mutate(child1)
            child2 = mutate(child2)

            # Add the children to the new population if they are valid
            if calculateWeight(child1, items) <= max_weight:
                new_population.append(child1)
            if calculateWeight(child2, items) <= max_weight:
                new_population.append(child2)

        population = new_population

    # Get the best individual
    best_individual = population[fitness.index(max(fitness))]
    print("Test case {}:".format(t + 1))
    print("Total Weight: {}".format(calculateWeight(best_individual, items)))
    print("Total Value: {}".format(calculateFitness(best_individual, items)))
    print("Selected Items:")
    for i in range(len(best_individual)):
        if best_individual[i] == 1:
            print("Item {}, weight {}, value {}".format(
                i + 1, items[i][0], items[i][1]))


t = int(inputNonEmpty())
for i in range(t):
    doWork(i)
