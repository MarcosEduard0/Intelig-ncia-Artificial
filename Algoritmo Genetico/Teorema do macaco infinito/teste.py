from populacao import Populacao


def algoritmoGenetico(n_populacao, n_individuo, p_cross, p_mut, elitismo=False, modelo=''):
    populacao = Populacao(n_populacao, n_individuo,
                          p_cross, p_mut, elitismo, modelo)
    geracao = 1
    while True:
        populacao = Populacao(
            n_populacao, n_individuo, p_cross, p_mut, elitismo, modelo, populacao.populacaoFinal)

        for pop in populacao.populacaoFinal:
            if not pop.fitness:
                print('Geração {}:  {}'.format(
                    geracao, pop.string))
                return
        print('Geração {}:  {}'.format(
            geracao, populacao.populacaoFinal[0].string))
        geracao += 1


string = input('Digite o modelo: ')

num_populacao = 200
tam_individuo = len(string)
porc_cross = 0.7
porc_mutacao = 0.05
porc_elitismo = 0.05

algoritmoGenetico(num_populacao, tam_individuo, porc_cross,
                  porc_mutacao, porc_elitismo, string)


# eu gostaria muito de passar na disciplina de inteligencia artificial com 10 na media!


# def criarPopulacao():
#     return [Individuo(6, 'marcos') for _ in range(2)]


# x = criarPopulacao()
# for i in zip(x[0].string, x[1].string):
#     print(i)
