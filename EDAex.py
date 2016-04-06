from random import Random
from time import time
import inspyred

class Lista(object):
    def __init__(self, index, value):
        self.value = value      #valor na permutação
        self.index = index      #valor na posicao

        #solucao
        #permutacao
        #quantas chamadas a funcao objetivo
def main(prng=None, display=False):


    cities = [ [37, 52], [49, 49], [52, 64], [20, 26], [40, 30] ]
    cities_tour = [i for i in range(len(cities))]

    #vai gerar as permutacoes iniciais das cidades
    #editar depois
    def my_generator(random, args):
        locations = cities_tour
        random.shuffle(locations)
        return locations

    def radixSort(array):
        result_parcial = [[] for i in range(10)]
        result_final = []

        #obtem o tamanho máximo de numero de algorismos do maior
        max = 0
        for i in range(len(array)):
            if array[i] > array[max]:
                max = i

        #resultado final recebe elementos com objeto index origin e valor
        #valor para ordenar e index para guardar a posição q deve mudar
        for i in range(len(array)):
            elm = Lista(i, array[i])
            result_final.append(elm)

        size = 1
        mod = 10
        max = array[max]
        find = False
        while not find:
            if max%mod == max:
                find = True
            else:
                mod = mod * 10
                size = size + 1

        m = 10
        n = 1
        for i in range(size):
            result_parcial = [[] for s in range(10)]
            for j in range(len(result_final)):
                value = result_final[j].value % m
                value = int(value/n)
                result_parcial[value].append(result_final[j])

            m = m*10
            n = n*10


            result_final = []
            pos_res_fin = 0
            for j in range(len(result_parcial)):
                for k in range(len(result_parcial[j])):
                    result_final.append(result_parcial[j][k])
                    pos_res_fin = pos_res_fin + 1

        perm = [-1 for i in range(len(array))]
        for i in range(len(perm)):
            perm[result_final[i].index] = i

        return perm

    #vai avaliar o fitness de cada canditato
    #para q o evol comp faca o servico
    def my_evaluator(candidates, args):
        #primeiro transformar  a lista de reais para uma de inteiros
        #multiplicar os valores por 100 para manter os inteiros reais

        fitness = []
        permute = []
        for cand in candidates:
            to_radix_pos = []
            to_radix_neg = []
            for i in range(len(cand)):
                #if(cand[i] > 0):
                to_radix_pos.append(int(cand[i]*100))
            permute = radixSort(to_radix_pos)

            print(permute)

            total = 0
            for i in range(0, len(permute)):
                total += permute[i]
            fitness.append(total)
        return fitness

    #somente ir pro git

    #usar isso aqui para alterar oq eu quero ver de dentro da evolucao
    #depois somente por
    #ea.observer = my_observer
    def my_observer(population, num_generations, num_evaluations, args):
        best = max(population)
        print("gen: %s fit: %s cand: %s prop: %s" % (num_generations, best.fitness, str(best.candidate), len(population)))

    #uso para finalizar a busca
    def my_terminator(population, num_generations, num_evaluations, args):
        max_generations = args.setdefault('max_generations', 1)
        return num_generations >= max_generations

    #funcao para fazer a variacao de dados
    #utiliza o gaussian proprio do framework, so tem q ver oq eh esse bounder
    #inspyred.ec.variators.gaussian_mutation

    #funcao para selecionar os meus itens
    #o metodo de selecao eh o prorpio do inspyred, ja que querermo selecionar toda a populcao
    #inspyred.ec.selectors.default_selection


    #funcao para recolocador dos itens
    #o metodo utilizado do proprio inspyred para recolocacao ( comma_replacement - seleciona de forma elitista )
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