from random import Random
import time
import inspyred
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation


#solucao
#permutacao
#quantas chamadas a funcao objetivo

class Lista(object):
    def __init__(self, index, value):
        self.value = value      #valor na permutacao
        self.index = index      #valor na posicao
        self.negative = False
        if value >= 0:
            self.negative = False
        else:
            self.negative = True
            self.value = self.value * (-1)


def main(prng=None, display=False):
    cities = []
    print ("Type the filename:")
    #Caminho usado pelo pc de Fernando
    #file_path = "/Users/Fenando/GitHub/TSP/Eil/eil51.tsp"
    #Caminho usado pelo pc de Gleidson
    file_path = "/Users/gmend/Documents/Dev/TSP/Eil/eil51.tsp"
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

    cities_tour = [i for i in range(51)]
    list_of_Xs = [[]]
    list_of_Ys = [[]]
    cities_choosen_x = []
    cities_choosen_y = []

    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)

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
        #valor para ordenar e index para guardar a posicao q deve mudar
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

        #obtem o tamanho maximo de numero de algorismos do maior
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
                city1 = cities[permute[i]-1]
                city2 = cities[permute[i+1]-1]
                sol = eu_dist(city1, city2)
                total = total + sol
            city1 = cities[permute[len(permute)-1]-1]
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
    def my_variator1(random, candidates, args):
        num_offspring = args.setdefault('num_offspring', 1)
        mut_rate = args.setdefault('mutation_rate', 0.1)

        num_genes = max([len(x) for x in candidates])
        genes = [[x[i] for x in candidates] for i in range(num_genes)]
        mean = [float(sum(x)) / float(len(x)) for x in genes]

        #stev
        stdev = []
        for g, m in zip(genes, mean):
            som = 0
            for x in g:
                som = som + ((x - m)**2)
            som = som/len(g)
            som = math.sqrt(som)
            stdev.append(som)

        mutants = []

        for i, cs in enumerate(candidates):
            mutant = copy.copy(cs)
            for j, (m, s) in enumerate(zip(mean, stdev)):
                if random.random() < mut_rate:
                        mutant[j] += random.gauss(m, s)
            mutants.append(mutant)
        return mutants

    def my_variator2(random, candidates, args):
        num_offspring = args.setdefault('num_offspring', 1)

        num_genes = max([len(x) for x in candidates])
        genes = [[x[i] for x in candidates] for i in range(num_genes)]
        mean = [float(sum(x)) / float(len(x)) for x in genes]

        #stev
        stdev = []
        for g, m in zip(genes, mean):
            som = 0
            for x in g:
                som = som + ((x - m)**2)
            som = som/len(g)
            som = math.sqrt(som)
            stdev.append(som)

        offspring = []
        for i in range(num_offspring):
            child = copy.copy(candidates[0])
            for i, (m, s) in enumerate(zip(mean, stdev)):
                child[i] = random.gauss(m, s)
            #child = bounder(child, args)
            offspring.append(child)
        return offspring

    def my_variator3(random, candidates, args):
        mutants = []
        for i, cs in enumerate(candidates):

            mut_rate = args.setdefault('mutation_rate', 0.1)
            mean = args.setdefault('gaussian_mean', 0.0)
            stdev = args.setdefault('gaussian_stdev', 1.0)
        #    bounder = args['_ec'].bounder
            mutant = copy.copy(cs)

            for j, m in enumerate(mutant):
                if random.random() < mut_rate:
                    mutant[j] += random.gauss(mean, stdev)
        #    mutant = bounder(mutant, args)

            mutants.append(mutant)
        return mutants
        #inspyred_mutator.single_mutation = mutate

    #funcao para fazer a variacao de dados
    #utiliza o gaussian proprio do framework, so tem q ver oq eh esse bounder
    #inspyred.ec.variators.gaussian_mutation

    #funcao para selecionar os meus itens
    #o metodo de selecao eh o prorpio do inspyred, ja que querermo selecionar toda a populcao
    #inspyred.ec.selectors.default_selection


    #funcao para recolocador dos itens
    #o metodo utilizado do proprio inspyred para recolocacao ( comma_replacement - seleciona de forma elitista )
    #inspyred.ec.replacers.comma_replacement

    def list_of_answer(perm):
        permute = radixSortPlusMinus(perm)


    if prng is None:
        prng = Random()
        prng.seed(time.time())

    ea = inspyred.ec.EDA(prng)

    ea.observer = my_observer
    ea.terminator = inspyred.ec.terminators.evaluation_termination

    #ea.selector = inspyred.ec.selectors.default_selection

    #ea.variator = my_variator1
    #ea.variator = my_variator2
    #ea.variator = my_variator3
    ea.variator = inspyred.ec.variators.gaussian_mutation

    #ea.replacer = inspyred.ec.replacers.comma_replacement

    #final_pop = ea.evolve(evaluator=my_evaluator,
    #                      generator=my_generator,
    #                      pop_size=100,
    #                      maximize=False,
    #                      #bounder=inspyred.ec.Bounder(0, 1),
    #                      max_evaluations=200000,
    #                      num_selected=100,
    #                      num_offspring=100,
    #                      num_elites=75)

    final_pop = ea.evolve(evaluator=my_evaluator,
                          generator=my_generator,
                          pop_size=100,
                          maximize=False,
                          #bounder=inspyred.ec.Bounder(0, 1),
                          max_evaluations=2000,
                          num_selected=100,
                          num_offspring=100,
                          num_elites=75)


    if display:
        best = max(final_pop)
        permute = best.candidate
        permute = radixSortPlusMinus(permute)
        for i in range(len(permute)):
            cities_choosen_x.append(cities[permute[i]][0])
            cities_choosen_y.append(cities[permute[i]][1])

        ani = animation.FuncAnimation(fig, animate, interval=1000)
        plt.show()



        print('hihi Best Solution: \n{0}'.format(str(best)))
    return ea

if __name__ == '__main__':
    main(display=True)