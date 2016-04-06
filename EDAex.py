from random import Random
from time import time
import inspyred
import math

#solucao
#permutacao
#quantas chamadas a funcao objetivo

class Lista(object):
    def __init__(self, index, value):
        self.value = value      #valor na permutação
        self.index = index      #valor na posicao
        self.negative = False
        if value >= 0:
            self.negative = False
        else:
            self.negative = True
            self.value = self.value * (-1)

def main(prng=None, display=False):


    cities = [
[37, 52],
[49, 49],
[52, 64],
[20, 26],
[40, 30],
[21, 47],
[17, 63],
[31, 62],
[52, 33],
[51, 21],
[42, 41],
[31, 32],
[5, 25],
[12, 42],
[36, 16],
[52, 41],
[27, 23],
[17, 33],
[13, 13],
[57, 58],
[62, 42],
[42, 57],
[16, 57],
[8, 52],
[7, 38],
[27, 68],
[30, 48],
[43, 67],
[58, 48],
[58, 27],
[37, 69],
[38, 46],
[46, 10],
[61, 33],
[62, 63],
[63, 69],
[32, 22],
[45, 35],
[59, 15],
[5, 6],
[10, 17],
[21, 10],
[5, 64],
[30, 15],
[39, 10],
[32, 39],
[25, 32],
[25, 55],
[48, 28],
[56, 37],
[30, 40]
               ]
    cities_tour = [i for i in range(len(cities))]
    mine = [
1,
22,
8,
26,
31,
28,
3,
36,
35,
20,
2,
29,
21,
16,
50,
34,
30,
9,
49,
10,
39,
33,
45,
15,
44,
42,
40,
19,
41,
13,
25,
14,
24,
43,
7,
23,
48,
6,
27,
51,
46,
12,
47,
18,
4,
17,
37,
5,
38,
11,
32
            ]

    #vai gerar as permutacoes iniciais das cidades
    #editar depois
    def my_generator(random, args):
        #para fazer o tour, nao excluir
        #locations = cities_tour
        #random.shuffle(locations)

        #um outro modo
        locations = [random.gauss(0, 1) for i in range(len(cities_tour))]

        return locations

    def radixSortPlusMinus(array):
        positivo = []
        negativo = []
        real_array = []

        #resultado final recebe elementos com objeto index origin e valor
        #valor para ordenar e index para guardar a posição q deve mudar
        for i in range(len(array)):
            elm = Lista(i, array[i])
            if elm.negative:
                negativo.append(elm)
            else:
                positivo.append(elm)

        if len(negativo) > 0:
            negativo = radixSort(negativo)
            for i in range(int(len(negativo)/2)):
                aux = negativo[i]
                negativo[i] = negativo[(len(negativo)-1)-i]
                negativo[(len(negativo)-1)-i] = aux
        if len(positivo) > 0:
            positivo = radixSort(positivo)

        real_array = negativo + positivo

        perm = [-1 for i in range(len(array))]
        for i in range(len(perm)):
            perm[real_array[i].index] = i

        return perm


    def radixSort(array):
        result_parcial = [[] for i in range(10)]
        result_final = array

        #obtem o tamanho máximo de numero de algorismos do maior
        max = 0
        for i in range(len(array)):
            if array[i].value > array[max].value:
                max = i

        size = 1
        mod = 10
        max = array[max].value
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
            for j in range(len(result_parcial)):
                for k in range(len(result_parcial[j])):
                    result_final.append(result_parcial[j][k])

        return result_final

    def eu_dist(p1, p2):
        val1 = math.pow ((p1[0] - p2[0]), 2)
        val2 = math.pow ((p1[1] - p2[1]), 2)
        d = math.sqrt (val1 + val2)
        return d

    #vai avaliar o fitness de cada canditato
    #para q o evol comp faca o servico
    def my_evaluator(candidates, args):
        #primeiro transformar  a lista de reais para uma de inteiros
        #multiplicar os valores por 100 para manter os inteiros reais
        fitness = []
        for cand in candidates:
            to_radix_pos = []
            permute = []
            for i in range(len(cand)):
                to_radix_pos.append(int(cand[i]*100))
            permute = radixSortPlusMinus(to_radix_pos)

            total = 0
            for i in range(0, len(permute)-1):
                city1 = cities[permute[i]]
                city2 = cities[permute[i+1]]
                sol = eu_dist(city1, city2)
                total = total + sol
            city1 = cities[permute[len(permute)-1]]
            city2 = cities[permute[0]]
            sol = eu_dist(city1, city2)
            total = total + sol

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
        max_generations = args.setdefault('max_generations', 100)
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
    ea.terminator = inspyred.ec.terminators.evaluation_termination

    #ea.selector = inspyred.ec.selectors.default_selection
    #ea.variator = inspyred.ec.variators.gaussian_mutation
    #ea.replacer = inspyred.ec.replacers.comma_replacement

    final_pop = ea.evolve(evaluator=my_evaluator,
                          generator=my_generator,
                          pop_size=200,
                          maximize=False,
                          max_evaluations=40000,
                          num_selected=200,
                          num_offspring=400,
                          num_elites=1)


    if display:
        best = max(final_pop)
        print('hihi Best Solution: \n{0}'.format(str(best)))
    return ea

if __name__ == '__main__':
    main(display=True)