import random
import string as s


class Individuo:

    def __init__(self, n, modelo='', string=''):
        self.n = n
        self.modelo = modelo
        self.string = string or self.gerarIndividuo()
        self.fitness = self.calcular_fitness()

    def gerarIndividuo(self):
        string = ''
        letras = s.ascii_letters + ' ' + s.punctuation + s.digits
        for _ in range(self.n):
            string += random.choice(letras)
        return string

    def calcular_fitness(self):
        fitness = 0
        for i in range(self.n):
            if self.string[i] != self.modelo[i]:
                fitness += 1
        return fitness
