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
        if current_line.startswith('DIMENSION'):
            n_cities = int(current_line.split(':')[1])  # pega a segunda parte da string

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

    cities = [

        [1000, 1000],
[1000, 3000],
[1000, 5000],
[2000, 6000],
[4000, 6000],
[6000, 6000],
[6000, 4000],
[6000, 2000],
[5000, 1000],
[3000, 1000]

    ]

    cities_tour = [i for i in range(len(cities))]
    list_of_best_city = []
    fit_over_gen = []

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
    def my_evaluator1(candidates, args):
        #primeiro transformar  a lista de reais para uma de inteiros
        #multiplicar os valores por 100 para manter os inteiros reais
        fitness = []
        for cand in candidates:
            to_radix_pos = []
            permute = []
            for i in range(len(cand)):
                to_radix_pos.append(int(cand[i]*10000))
            permute = radixSortPlusMinus(to_radix_pos)

            total = calcDistancia(permute)

            fitness.append(total)
        return fitness

    #vai avaliar o fitness de cada canditato
    #para q o evol comp faca o servico
    def my_evaluator2(candidates, args):
        #primeiro transformar  a lista de reais para uma de inteiros
        #multiplicar os valores por 100 para manter os inteiros reais
        fitness = []
        for cand in candidates:
            to_radix_pos = []
            permute = []
            for i in range(len(cand)):
                to_radix_pos.append(int(cand[i]*10000))
            permute = radixSortPlusMinus(to_radix_pos)

            total = calcDistancia(permute)

            fitness.append(total)
        return fitness

    def cause_to_termination(population, num_generations, num_evaluations, args):
        finish = False
        best = max(population)
        max_evaluations = args.setdefault('max_evaluations', len(population))

        if num_evaluations >= max_evaluations:
            finish = True

        if finish:
            return True

        return False

    def calcDistancia(permute):
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
        return total

    def calcDistancia2(permute):
        total = 0
        for i in range(0, len(permute)-1):
            index1 = permute[i]-1#-1
            index2 = permute[i+1]-1
            city1 = cities[index1]
            city2 = cities[index2]
            if (index1)%2 == 0 and (index2)%2 == 0:
                sol = eu_dist(city1, city2)/2
            else:
                sol = eu_dist(city1, city2)
            total = total + sol
        city1 = cities[permute[len(permute)-1]-1]
        city2 = cities[permute[0]]
        sol = eu_dist(city1, city2)
        total = total + sol
        return total
    #somente ir pro git

    #usar isso aqui para alterar oq eu quero ver de dentro da evolucao
    #depois somente por
    #ea.observer = my_observer
    def my_observer(population, num_generations, num_evaluations, args):
        best = max(population)
        list_of_best_city.append(best.candidate)
        fit_over_gen.append(best.fitness)
        print("gen: %s fit: %s evaluation: %s prop: %s" % (num_generations, best.fitness, num_evaluations, len(population)))


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

    def list_of_answer(perm):
        permute = radixSortPlusMinus(perm)

    def animate(i):
        xar = []
        yar = []
        # for i in range(len(list_of_best_city)):
        if(i < len(list_of_best_city)):
            permute = radixSortPlusMinus(list_of_best_city[i])
            st = "Rota %s "% permute
            st2 = "Fitness %s"% calcDistancia(permute)
            fig.suptitle(st, fontsize=19, fontweight='bold')
            ax1.set_title(st2)
        else:
            permute = radixSortPlusMinus(list_of_best_city[len(list_of_best_city)-1])
            st = "Rota %s "% permute
            st2 = "Fitness %s"% calcDistancia(permute)
            fig.suptitle(st, fontsize=19, fontweight='bold')
            ax1.set_title(st2)
        for j in range(len(permute)):
            xar.append(cities[permute[j]][0])
            yar.append(cities[permute[j]][1])
        xar.append(cities[permute[0]][0])
        yar.append(cities[permute[0]][1])

        ax1.clear()
        ax1.plot(xar,yar)

    if prng is None:
        prng = Random()
        prng.seed(time.time())

    ea = inspyred.ec.EDA(prng)

    ea.observer = my_observer
    ea.terminator = cause_to_termination
    ea.archiver = inspyred.ec.archivers.best_archiver

    ea.selector = inspyred.ec.selectors.default_selection

    #ea.variator = my_variator1
    #ea.variator = my_variator2
    #ea.variator = my_variator3
    ea.variator = inspyred.ec.variators.gaussian_mutation

    ea.replacer = inspyred.ec.replacers.truncation_replacement

    final_pop = ea.evolve(evaluator=my_evaluator1,
                          generator=my_generator,
                          pop_size=100,
                          maximize=False,
                          #bounder=inspyred.ec.Bounder(0, 1),
                          max_evaluations=100000,
                          num_selected=100,
                          num_offspring=100,
                          num_elites=75)


    if display:
        best = max(final_pop)
        permute = best.candidate
        list_of_best_city.append(permute)
        ani = animation.FuncAnimation(fig, animate, interval=100)
        plt.show()

        ani = []

        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1)
        xar = []
        yar = []
        permute = radixSortPlusMinus(permute)
        for j in range(len(permute)):
            xar.append(cities[permute[j]][0])
            yar.append(cities[permute[j]][1])
        xar.append(cities[permute[0]][0])
        yar.append(cities[permute[0]][1])
        ax1.plot(xar,yar)
        plt.show()

        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1)
        xar = []
        yar = []
        for j in range(len(fit_over_gen)):
            xar.append(j)
            yar.append(fit_over_gen[j])
        ax1.plot(xar,yar)
        plt.show()

        print('Fitness: %s Best Solution %s:' % (best.fitness, str(permute)))
        print(radixSortPlusMinus(permute))
    return ea

if __name__ == '__main__':
    main(display=True)