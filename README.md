# TSP com EDA
FERNANDO VERAS, GLEIDSON MENDES

#DOCUMENTAÇÃO

ESTE DOCUMENTO TEM O OBJETIVO DE EXPLANAR O PROCESSO DE DESENVOLVIMENTO DO
PROBLEMA DO CAIXEIRO VIAJANTE UTILIZANDO EDA
				
##def main(prng=None, display=False, file_path=None, make_lobat_problem=False, show_graphics=False)
        Para fazer a chamada do programa temos os seguintes parâmetros: forma de cálculo para números aleatórios,  
        se vai mostrar o resultado, endereço do arquivo, indicar se é pra utilizar o problema do lobato e se é parar mostrar os gráficos

#Chamadas diretas da framework

##Inicialização EDA
			Inicializa o processo de evolução. Passasse o avaliador e o gerador. Assim como o tamanho da pilha de filhos, definir se o problema é de maximização (neste caso é Falso - minimização), numero máximo de avaliações, máximo número de indivíduos a ser selecionado da população existente, número de filhos produzidos em uma geração e o número máximo de elite (não obrigatório no EDA))

      ea = inspyred.ec.EDA(prng)
      ea.observer = my_observer
      ea.terminator = cause_to_termination

      ea.selector = inspyred.ec.selectors.default_selection           \\ codigo da framework
      ea.variator = inspyred.ec.variators.gaussian_mutation						\\ codigo da framework
      ea.replacer = inspyred.ec.replacers.truncation_replacement			\\ codigo da framework
      
	    final_pop = ea.evolve(evaluator=my_evaluator1,
	                    generator=my_generator,
	                    pop_size=100,
	                    maximize=False,
	                    #bounder=inspyred.ec.Bounder(0, 1),
	                    max_evaluations=100000,
	                    num_selected=100,
	                    num_offspring=100,
	                    num_elites=75)
      
##def my_generator(random, args):
			 Definição de um generator próprio. Gera um indivíduo para a população inicial. Este indivíduo terá um valor real aleatório entre 0 e 1
			 
##def my_evaluator1(candidates, args):
			 Recebe o valor da distribuição de cada candidato da população, acha a permutação referente a distribuição e calcula o fitness da permutação
  
##def cause_to_termination(population, num_generations, num_evaluations, args):
			Função de checagem se já é possível finalizar. Neste caso, finalizasse se o numero de avaliações chegar no máximo ou se o valor do fitness estacionar no mesmo valor por muito tempo

##def my_observer(population, num_generations, num_evaluations, args):
			Possibilita ver o status da evolução em tempo de execução

##variators
			alterações próprias dos métodos de variação dos individuos
			def my_variator1(random, candidates, args):
			def my_variator2(random, candidates, args):
			def my_variator3(random, candidates, args):				
			
#Algoritmos de suporte

##class Lista(object)
			Classe criada para a resolução do radix sort proposto sem utilização de uma organização com loops encadeados
				
##def radixSortPlusMinus(array):
			Executa o algoritmo radix sort seprando os valores positivos e negativos e então aplica-se radix sort em cada um, obtendo um vetor resultante com a junção dos 2 resultados.
			2 problemas são identificados com este sort é que, ele só ordena valores inteiros e positivos. Assim antes ser aplicado o radix sort, devemos tratar os valores reais e/ou negativos.
			Antes da entrada dessa função:
			     Para tratar de reais para inteiros, multiplicasse cada valor por algum múltiplo de 10 aumentando assim o número inteiro e somente esse número inteiro é passado para o radix sort. Assim com os valores : -1.23*100 = -123; 0.05*100 = 5; 0.17*100 = 17
			Na função:
			     Para tratar de negativos para positivos, é feito uma separação de array. Um array conterá somente valores positivos e outro somente valores negativos e então cada array é passado para ser ordenado pelo radix sort. No final, o array negativo organizado do menor para o maior é aplicado uma ordem inversa e então juntado ao array positivo.
			Ao termino:
					Ao fim disso tudo temos um array ordenado. Por se tratar de uma ordenação, os valores ficaram do menor para o maior. Assim, ordenando os valores, não possuimos uma rota resultando pois o resultado final seria 0,1,2 ... N. Onde é criada uma classe que possui o index no vetor original e o valor. Ordena-se pelo valor e organiza-se pelo index. Ou seja, a permutação resultante ver em qual posição do vetor original apareceu o menor valor. Então é posto na posição do menor valor o index do vetor original
					
##def radixSort(array):
			Executa o algoritmo do radix sort em si, sobre numeros inteiros e positivos.
			o radix sort analisa cada algorismo do numero no vetor para fazer a ordenação. Ao multiplicar a variável Mod por múltiplos de 10 e ao fazer a operação de mod, vamos separando os valores por sua significância. E depois a divisão do resultado do mod pela variável Divisor, temos a posição no array parcial. Assim ordena-se por unidades, dezenas, centenas, e assim por diante.
			
##def eu_dist(p1, p2):
			Calcula distancia euclidiana entre 2 pontos bidimensionais
			
##def calcDistancia(permute):
			Calcula o somatório de todas as distancias euclidianas a cada 2 pontos na ordem que as cidades aprecem na permutação.
			Obs: para o problema do lobato, quando 2 cidades são pares, o valor euclidiano entre aquelas 2 cidades é pela metade
			
##def animate(i):
			Utiliado pela função gráfica para o desenho
			
##Análise
			Composição de análise dos resultados
			def somar(valores):
			def media(valores):
			def variancia(valores):
			def desvio_padrao(valores):
			

			
