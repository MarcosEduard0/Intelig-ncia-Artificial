import random
import time
POPULATION_SIZE = 100   # Number of individuals in each generation
ELITISM_RATE = 0.05  # Percentage of the fittest individuals that will survive
# Number of the fittest individuals that will generate the new population
SELECTION_SIZE = 35
MUTATION_RATE = 0.05  # Probability of mutation

# Valid genes: Valid chars
GENES = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890, .-;:_!"#%&/()=?@${[]}'

# Target string to be generated
DEFAULT_TARGET = input('Digite o modelo: ')
# DEFAULT_TARGET = 'eu gostaria muito de passar na disciplina de inteligencia artificial com 10 na media!'


class Individual(object):
    def __init__(self, genotype=''):
        self.genotype = genotype or self.__create_genotype()
        self.fitness = self.__calculate_fitness()

    def __create_genotype(self):
        '''
        Create genotype or string of genes
        '''
        global DEFAULT_TARGET
        genotype_len = len(DEFAULT_TARGET)
        return [self.__generate_mutated_gene() for _ in range(genotype_len)]

    def __generate_mutated_gene(self):
        '''
        Create random gene
        '''
        global GENES
        gene = random.choice(GENES)
        return gene

    def __calculate_fitness(self):
        '''
        Calculate fitness score
        '''
        global DEFAULT_TARGET
        fitness = 0
        for individual_gene, target_gene in zip(self.genotype, DEFAULT_TARGET):
            if individual_gene != target_gene:
                fitness += 1
        return fitness

    def reproduce(self, partner):
        '''
        Perform breeding and produce offspring
        '''
        global MUTATION_RATE

        self_gene_threshold = 1 - MUTATION_RATE

        partner_gene_threshold = self_gene_threshold / 2

        # genotype for the new individual
        child_genotype = []
        for self_gene, partner_gene in zip(self.genotype, partner.genotype):

            # random probability
            probability = random.random()

            # Crossover
            if probability < self_gene_threshold:
                child_genotype.append(partner_gene)
            elif probability < partner_gene_threshold:
                child_genotype.append(self_gene)

            # Mutation
            else:
                child_genotype.append(self.__generate_mutated_gene())

        return Individual(child_genotype)


def main():
    global POPULATION_SIZE
    global ELITISM_RATE
    global SELECTION_SIZE

    generation = 1

    found = False
    population = []

    # create initial population
    for _ in range(POPULATION_SIZE):
        population.append(Individual())

    def print_status(generation, fitness, genotype):
        print("Geração {}:  {}".format(
            generation, "".join(genotype)))

    while not found:
        # Sort the population in increasing order of fitness score
        population = sorted(population, key=lambda x: x.fitness)

        # If the fittest individual genotype matches
        # the desired one, finish the program
        if population[0].fitness <= 0:
            found = True
            break

        new_generation = []

        # Perform Elitism
        elitism_size = int(ELITISM_RATE * POPULATION_SIZE)
        new_generation.extend(population[:elitism_size])

        # Generate the new individuals
        generated_individuals_size = POPULATION_SIZE - elitism_size
        for _ in range(generated_individuals_size):
            parent_1 = random.choice(population[:SELECTION_SIZE])
            parent_2 = random.choice(population[:SELECTION_SIZE])
            child = parent_1.reproduce(parent_2)

            new_generation.append(child)

        population = new_generation

        print_status(generation, population[0].fitness, population[0].genotype)

        generation += 1

    print_status(generation, population[0].fitness, population[0].genotype)


if __name__ == '__main__':
    main()
