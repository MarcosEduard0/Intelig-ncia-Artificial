from individuo import Individuo
import string as s
import random


class Populacao:

    def __init__(self, n, n_individuo, p_crossover, p_mutacao, elitismo=False,  modelo='', individuos=[]):
        self.n = n
        self.letras = s.ascii_letters + ' ' + s.punctuation + s.digits
        self.n_individuo = n_individuo
        self.modelo = modelo
        self.p_crossover = p_crossover
        self.p_mutacao = p_mutacao
        self.elitismo = elitismo
        self.individuos = individuos or self.criarPopulacao()
        self.popIntermediaria = self.gerarPopulacaoIntermediaria()
        self.popIntermediaria = self.Crossover_Mutacao()
        if elitismo:
            self.populacaoFinal += self.popIntermediaria[(
                int(self.elitismo * self.n)):]
        else:
            self.populacaoFinal = self.popIntermediaria

    def criarPopulacao(self):
        return [Individuo(self.n_individuo, self.modelo) for _ in range(self.n)]

    def gerarPopulacaoIntermediaria(self):
        individuos = []
        self.individuos = sorted(
            self.individuos, key=lambda x: x.fitness)

        if self.elitismo:
            elitism_size = int(self.elitismo * self.n)
            self.populacaoFinal = individuos.copy()
            self.populacaoFinal = self.populacaoFinal + \
                self.individuos[:elitism_size]

        # proprio_gene_select = 1 - self.p_mutacao
        # parceiro_gene_select = proprio_gene_select / 2

        # Seleção por torneio
        for _ in range(self.n):
            probability = random.random()

            random1 = random.randint(0, self.n-1)
            random2 = random.randint(0, self.n-1)
            if probability < 0.5:
                individuos.append(self.individuos[random1])
            else:
                individuos.append(self.individuos[random2])

        return individuos

    def Crossover_Mutacao(self):
        '''Realização do corte de forma aleatória.'''
        individuos = []
        for i in range(0, self.n, 2):
            if random.random() < self.p_crossover:
                corte1 = random.randint(0, self.n_individuo-1)
                corte2 = random.randint(corte1+1, self.n_individuo)
                pai1 = self.popIntermediaria[i].string
                pai2 = self.popIntermediaria[i+1].string
                filho1 = pai1[:corte1] + pai2[corte1:corte2]+pai1[corte2:]
                filho2 = pai2[:corte1]+pai1[corte1:corte2]+pai2[corte2:]
                novoIndividuo1 = Individuo(
                    self.n_individuo, self.modelo, filho1)
                novoIndividuo2 = Individuo(
                    self.n_individuo, self.modelo, filho2)
                individuos.append(self.Mutacao(novoIndividuo1))
                individuos.append(self.Mutacao(novoIndividuo2))
            else:
                individuos.append(self.Mutacao(self.popIntermediaria[i]))
                individuos.append(self.Mutacao(self.popIntermediaria[i + 1]))

        return individuos

    def Mutacao(self, individuo):
        if random.random() < self.p_mutacao:
            randomIndex = random.randint(0, self.n_individuo-1)
            string = individuo.string.replace(
                individuo.string[randomIndex], random.choice(self.letras))
            return Individuo(self.n_individuo, self.modelo, string)
        return individuo
