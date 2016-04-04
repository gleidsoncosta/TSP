from random import Random
from time import time
import inspyred

def main(prng=None, display=False):

    #vai gerar as permutacoes iniciais das cidades
    #editar depois
    def my_generator(random, args):
        locations = [i for i in range(0, 4)]
        random.shuffle(locations)
        return locations

    #vai avaliar o fitness de cada canditato
    #para q o evol comp faca o servico
    def my_evaluator(candidates, args):
        fitness = []
        for candidate in candidates:
                total = 0
                for i in range(0, len(candidate)):
                    total += candidate[i]
                fitness.append(total)
        return fitness

    #usar isso aqui para alterar oq eu quero ver de dentro da evolução
    #depois somente por
    #ea.observer = my_observer
    def my_observer(population, num_generations, num_evaluations, args):
        best = max(population)
        print("gen: %s fit: %s cand: %s prop: %s" % (num_generations, best.fitness, str(best.candidate), len(population)))

    #uso para finalizar a busca
    def my_terminator(population, num_generations, num_evaluations, args):
        max_evaluations = args.setdefault('max_evaluations', len(population))
        return num_evaluations >= max_evaluations

    #funcao para fazer a variacao de dados
    #utiliza o gaussian proprio do framework, so tem q ver oq é esse bounder
    #inspyred.ec.variators.gaussian_mutation

    #funcao para selecionar os meus itens
    #o metodo de selação é o prorpio do inspyred, ja que querermo selecionar toda a populcao
    #inspyred.ec.selectors.default_selection


    #funcao para recolocador dos itens
    #o metodo utilizado do proprio inspyred para recolocação ( comma_replacement - seleciona de forma elitista )
    #inspyred.ec.replacers.comma_replacement



    if prng is None:
        prng = Random()
        prng.seed(time())

    ea = inspyred.ec.EDA(prng)

    ea.observer = my_observer
    ea.terminator = my_terminator

    ea.selector = inspyred.ec.selectors.default_selection
    ea.variator = inspyred.ec.variators.gaussian_mutation
    ea.replacer = inspyred.ec.replacers.comma_replacement

    final_pop = ea.evolve(evaluator=my_evaluator,
                          generator=my_generator,
                          pop_size=500,
                          max_evaluations=15000,
                          num_selected=500,
                          num_offspring=500,
                          num_elites=1)


    if display:
        best = max(final_pop)
        print('hihi Best Solution: \n{0}'.format(str(best)))
    return ea

if __name__ == '__main__':
    main(display=True)