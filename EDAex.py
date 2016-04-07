from random import Random
from time import time
import inspyred

#solucao
#permutacao
#quantas chamadas a funcao objetivo

class Lista(object):
    def __init__(self, index, value):
        self.value = value      #valor na permutacao
        self.index = index      #valor na posicao

def main(prng=None, display=False):
    cities = []
    print "Type the filename:"
    #file_path = "../Eil/eil51.tsp"
    file_path = "/Users/Fenando/GitHub/TSP/Eil/eil51.tsp"
    # file_name = raw_input("> ")
    file_name = file_path

    with open(file_name) as f:
        lines = f.readlines()

    n_cities = 0
    for i in range(2, len(lines)):  # Esse for busca o numero de cidades
        current_line = str(lines[i])
        if current_line.startswith('DIMENSION :'):
            str_n_cities = current_line.split(':')[1]  # pega a segunda parte da string
            while str_n_cities.startswith(' '):  # remove qualquer espaco no comeco
                str_n_cities = str_n_cities[1: len(str_n_cities)]
            if str_n_cities.endswith("\\") or str_n_cities.endswith(' '):  # remove qualquer barra ou espaco no final
                str_n_cities = str_n_cities[0: (len(str_n_cities) - 2)]
            n_cities = int(str_n_cities)
            break
    print(n_cities)
    points_start = False  # armazena se a seccao que lista os pontos comecou
    for j in range(i + 1, (len(lines) - 1)):  # esse for busca os pontos
        s = str(lines[j])
        if points_start and not (s.startswith('EOF')):
            xCoord = float(s.split(" ")[1])
            yCoord = float(s.split(" ")[2])
            cities.append([xCoord, yCoord])
        if s.startswith('NODE_COORD_SECTION'):  # a seccao que lista os pontos comeca na prox linha
            points_start = True

    cities_tour = [i for i in range(len(cities))]
    mine = [1,
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
32]

    #vai gerar as permutacoes iniciais das cidades
    #editar depois
    def my_generator(random, args):
        locations = cities_tour
        random.shuffle(locations)

        #my_sol = 0
        #for i in range(0, len(mine)-1):
        #    my_sol += eu_dist(cities[mine[i]], cities[mine[i+1]])
        #my_sol += eu_dist(cities[mine[len(mine)-1]], cities[mine[0]])

        #print("minha solucao %s" % my_sol)

        return locations

    def radixSort(array):
        result_parcial = [[] for i in range(10)]
        result_final = []

        #obtem o tamanho maximo de numero de algorismos do maior
        max = 0
        for i in range(len(array)):
            if array[i] > array[max]:
                max = i

        #resultado final recebe elementos com objeto index origin e valor
        #valor para ordenar e index para guardar a posicao q deve mudar
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

    def eu_dist(p1, p2):
        d = (((p1[0] - p2[0])**2)+((p1[1] - p2[1])**2))**(0.5)
        return d



    #vai avaliar o fitness de cada canditato
    #para q o evol comp faca o servico
    def my_evaluator(candidates, args):
        #primeiro transformar  a lista de reais para uma de inteiros
        #multiplicar os valores por 100 para manter os inteiros reais
        fitness = []
        for cand in candidates:
            to_radix_pos = []
            to_radix_neg = []
            permute = []
            for i in range(len(cand)):
                #if(cand[i] > 0):
                to_radix_pos.append(int(cand[i]*100))
            permute = radixSort(to_radix_pos)

            total = 0
            for i in range(0, len(permute)-1):
                total += eu_dist(cities[permute[i]], cities[permute[i+1]])
            total += eu_dist(cities[permute[len(permute)-1]], cities[permute[0]])

            #print(permute)

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
    ea.terminator = my_terminator

    ea.selector = inspyred.ec.selectors.default_selection
    ea.variator = inspyred.ec.variators.gaussian_mutation
    ea.replacer = inspyred.ec.replacers.comma_replacement

    final_pop = ea.evolve(evaluator=my_evaluator,
                          generator=my_generator,
                          pop_size=200,
                          max_evaluations=4000,
                          num_selected=200,
                          num_offspring=400,
                          num_elites=1)


    if display:
        best = max(final_pop)
        print('hihi Best Solution: \n{0}'.format(str(best)))
    return ea

if __name__ == '__main__':
    main(display=True)