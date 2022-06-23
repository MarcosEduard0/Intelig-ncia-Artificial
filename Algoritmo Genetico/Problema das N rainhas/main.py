# %%
import plotly.offline as py
import plotly.graph_objs as go
import numpy as np
import math
import random
import copy
# %%


class Individuo:

    def __init__(self, n, rainhas=[], binario=''):
        self.n = n
        self.bits = math.ceil(math.log(self.n, 2))
        if rainhas and not binario:
            self.rainhas = rainhas
            self.binario = self.convertDecimal2Binario()
        elif not rainhas and binario:
            self.binario = binario
            self.rainhas = self.convertBinario2Decimal()
        else:
            self.rainhas = self.gerarIndividuo()
            self.binario = self.convertDecimal2Binario()

        self.fitness = self.calcular_fitness()

    def gerarIndividuo(self):
        '''Função para gerar um tabuleiro com rainhas aleatórias.'''
        return [random.randint(1, self.n) for _ in range(self.n)]

    def convertBinario2Decimal(self):
        individuo = []
        for i in range(0, len(self.binario), self.bits):
            individuo.append(int(self.binario[i:i+self.bits], 2) + 1)
        return individuo

    def convertDecimal2Binario(self):
        binario = ''
        for e in self.rainhas:
            binario += format(e - 1, "b").zfill(self.bits)
        return binario

    def calcular_fitness(self):
        '''Calcula o fitness de um cromossomo'''
        ataques = 0
        max_ataques = self.n*(self.n-1)/2
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.rainhas[i] == self.rainhas[j]:
                    ataques += 1
                elif self.rainhas[i] + (j - i) == self.rainhas[j]:
                    ataques += 1
                elif self.rainhas[i] - (j - i) == self.rainhas[j]:
                    ataques += 1
        self.adptacao = max_ataques - ataques
        return max_ataques - ataques

# %%


class Populacao:

    def __init__(self, n, n_individuo, p_crossover, p_mutacao, elitismo=False, individuos=[]):
        self.n = n
        self.n_individuo = n_individuo
        self.p_crossover = p_crossover
        self.p_mutacao = p_mutacao
        self.elitismo = elitismo
        self.individuos = individuos or self.gerarPopulacao()
        self.probabilidades = self.RoletaViciada()
        self.popIntermediaria = self.Selecao()
        self.popIntermediaria = self.Crossover_Mutacao()

    def gerarPopulacao(self):
        individuos = []
        for _ in range(self.n):
            individuos.append(Individuo(self.n_individuo))
        return individuos

    def RoletaViciada(self):
        if hasattr(self, 'probabilidades'):
            return self.probabilidades
        probabilidades, media = [], []
        total = 0
        self.melhorIndividuo = copy.deepcopy(self.individuos[0])

        for individuo in self.individuos:
            total += individuo.fitness
            probabilidades.append(total)
            media.append(individuo.fitness)

            if individuo.fitness > self.melhorIndividuo.fitness:
                self.melhorIndividuo = copy.deepcopy(individuo)

        self.media = np.mean(media)
        probabilidades = list(
            map(lambda x: x/total, probabilidades))
        self.probabilidades = probabilidades
        return probabilidades

    def Selecao(self):
        individuos = []
        for _ in range(self.n):

            random = np.random.random()
            for i in range(len(self.probabilidades)):
                if self.probabilidades[i] > random:
                    individuos.append(self.individuos[i])
                    break

        if self.elitismo:
            individuos[0] = copy.deepcopy(self.melhorIndividuo)

        return individuos

    def Crossover_Mutacao(self):
        individuos = []
        for i in range(0, self.n, 2):
            if np.random.random() < self.p_crossover:
                # Crossover
                corte1 = random.randint(0, self.n_individuo-1)
                corte2 = random.randint(corte1+1, self.n_individuo)
                pai1 = self.popIntermediaria[i].rainhas
                pai2 = self.popIntermediaria[i+1].rainhas
                filho1 = pai1[:corte1] + pai2[corte1:corte2]+pai1[corte2:]
                filho2 = pai2[:corte1]+pai1[corte1:corte2]+pai2[corte2:]
                novoIndividuo1 = Individuo(self.n_individuo, filho1)
                novoIndividuo2 = Individuo(self.n_individuo, filho2)
                # Mutação
                individuos.append(self.Mutacao(novoIndividuo1))
                individuos.append(self.Mutacao(novoIndividuo2))
            else:
                individuos.append(self.Mutacao(self.popIntermediaria[i]))
                individuos.append(self.Mutacao(self.popIntermediaria[i + 1]))

        if self.elitismo:
            individuos[0] = copy.deepcopy(self.melhorIndividuo)

        return individuos

    def Mutacao(self, individuo):
        if np.random.random() < self.p_mutacao:
            select = np.random.randint(self.n_individuo)
            individuo.rainhas[select] = np.random.randint(
                1, self.n_individuo + 1)
            return Individuo(
                self.n_individuo, individuo.rainhas)
        return individuo

# %%


class PopulacaoBinaria:

    def __init__(self, n, n_individuo, p_crossover, p_mutacao, elitismo=False, individuos=[]):
        self.n = n
        self.n_individuo = n_individuo
        self.p_crossover = p_crossover
        self.p_mutacao = p_mutacao
        self.elitismo = elitismo
        self.individuos = individuos or self.gerarPopulacao()
        self.probabilidades = self.RoletaViciada()
        self.popIntermediaria = self.Selecao()
        self.popIntermediaria = self.Crossover_Mutacao()

    def gerarPopulacao(self):
        individuos = []
        for _ in range(self.n):
            individuos.append(Individuo(self.n_individuo))
        return individuos

    def RoletaViciada(self):
        if hasattr(self, 'probabilidades'):
            return self.probabilidades
        probabilidades, media = [], []
        total = 0
        self.melhorIndividuo = copy.deepcopy(self.individuos[0])

        for individuo in self.individuos:
            total += individuo.fitness
            probabilidades.append(total)
            media.append(individuo.fitness)

            if individuo.fitness > self.melhorIndividuo.fitness:
                self.melhorIndividuo = copy.deepcopy(individuo)

        self.media = np.mean(media)
        probabilidades = list(
            map(lambda x: x/total, probabilidades))
        self.probabilidades = probabilidades
        return probabilidades

    def Selecao(self):
        individuos = []
        for _ in range(self.n):

            random = np.random.random()
            for i in range(len(self.probabilidades)):
                if self.probabilidades[i] > random:
                    individuos.append(self.individuos[i])
                    break

        if self.elitismo:
            individuos[0] = copy.deepcopy(self.melhorIndividuo)

        return individuos

    def Crossover_Mutacao(self):
        individuos = []
        bits = math.ceil(math.log(self.n_individuo, 2))
        for i in range(0, self.n, 2):
            if np.random.random() < self.p_crossover:
                # Crossover
                corte1 = random.randint(0, (self.n_individuo-1)*bits)
                corte2 = random.randint(corte1+1, self.n_individuo*bits)

                pai1 = self.popIntermediaria[i].binario
                pai2 = self.popIntermediaria[i+1].binario
                filho1 = pai1[:corte1] + pai2[corte1:corte2]+pai1[corte2:]
                filho2 = pai2[:corte1]+pai1[corte1:corte2]+pai2[corte2:]
                novoIndividuo1 = Individuo(self.n_individuo, binario=filho1)
                novoIndividuo2 = Individuo(self.n_individuo, binario=filho2)

                # Mutação
                individuos.append(self.Mutacao(novoIndividuo1))
                individuos.append(self.Mutacao(novoIndividuo2))
            else:
                individuos.append(self.Mutacao(self.popIntermediaria[i]))
                individuos.append(self.Mutacao(self.popIntermediaria[i + 1]))

        if self.elitismo:
            individuos[0] = copy.deepcopy(self.melhorIndividuo)

        return individuos

    def Mutacao(self, individuo):
        bits = math.ceil(math.log(self.n_individuo, 2))
        if np.random.random() < self.p_mutacao:
            select = np.random.randint(0, bits*self.n_individuo)
            binario = list(individuo.binario)
            binario[select] = '1' if binario[select] == '0' else '0'
            return Individuo(
                self.n_individuo, binario=(''.join(binario)))
        return individuo


# %%

def algoritmoGeneticoBinario(total_geration, n_populacao, n_individuo, p_cross, p_mut, elitismo=False):
    melhores = []
    media, geracao = [], [0, ]
    populacao = PopulacaoBinaria(
        n_populacao, n_individuo, p_cross, p_mut, elitismo)
    melhores.append(populacao.melhorIndividuo.fitness)
    media.append(populacao.media)
    for i in range(total_geration):
        populacao = PopulacaoBinaria(
            n_populacao, n_individuo, p_cross, p_mut, elitismo, populacao.popIntermediaria)
        melhores.append(populacao.melhorIndividuo.fitness)
        media.append(populacao.media)
        geracao.append(i+1)

    print('Melhor individuo da última geração: {}\nAdaptação: {}'.format(
        populacao.melhorIndividuo.binario, populacao.melhorIndividuo.fitness))
    return geracao, melhores, media

# %%


def algoritmoGenetico(total_geration, n_populacao, n_individuo, p_cross, p_mut, elitismo=False):
    melhores = []
    media, geracao = [], [0, ]
    populacao = Populacao(n_populacao, n_individuo, p_cross, p_mut, elitismo)
    melhores.append(populacao.melhorIndividuo.fitness)
    media.append(populacao.media)
    for i in range(total_geration):
        populacao = Populacao(
            n_populacao, n_individuo, p_cross, p_mut, elitismo, populacao.popIntermediaria)
        melhores.append(populacao.melhorIndividuo.fitness)
        media.append(populacao.media)
        geracao.append(i+1)

    print('Melhor individuo da última geração: {}\nAdaptação: {}'.format(
        populacao.melhorIndividuo.rainhas, populacao.melhorIndividuo.fitness))
    return geracao, melhores, media


# %%
geracao = 2000
populacao = 100
rainhas = 32
p_cross = 0.7
p_mut = 0.03
elitismo = True
bin = True

if bin:
    geracao, melhores, media = algoritmoGeneticoBinario(
        geracao, populacao, rainhas, p_cross, p_mut, elitismo)
else:
    geracao, melhores, media = algoritmoGenetico(
        geracao, populacao, rainhas, p_cross, p_mut, elitismo)


trace1 = go.Scatter(x=geracao,
                    y=melhores,
                    mode='lines',
                    name='Melhores adaptações',
                    line={'color': '#ee5253'})

trace2 = go.Scatter(x=geracao,
                    y=media,
                    mode='lines',
                    name='Média da adaptação',
                    line={'color': '#30eb23'})
data = [trace1, trace2]

layout = go.Layout(
    autosize=False,
    width=600,
    height=400,
)

fig = go.Figure(data=data, layout=layout)


py.iplot(fig, filename='size-margins')
# py.iplot(data)

# %%
