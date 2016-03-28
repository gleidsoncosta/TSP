from random import Random
from time import time
import math
import inspyred


def main(prng=None, display=False):
    if prng is None:
        prng = Random()
        prng.seed(time())

    points = [(110.2, 225.3), (161.0, 280.7), (325.05, 554.03), (490.2, 285.9),
              (157.04, 443.04), (283.05, 379.07), (397.60, 566.70), (306.08, 360.1),
              (343.03, 110.10), (552.40, 199.50)]
    weights = [[0 for _ in range(len(points))] for _ in range(len(points))]
    for i, p in enumerate(points):
        for j, q in enumerate(points):
            weights[i][j] = math.sqrt((p[0] - q[0])**2 + (p[1] - q[1])**2)

    problem = inspyred.benchmarks.TSP(weights)
    ac = inspyred.swarm.ACS(prng, problem.components)
    ac.terminator = inspyred.ec.terminators.generation_termination
    final_pop = ac.evolve(generator=problem.constructor,
                          evaluator=problem.evaluator,
                          bounder=problem.bounder,
                          maximize=problem.maximize,
                          pop_size=10,
                          max_generations=50)

    if display:
        best = max(ac.archive)
        print('Best Solution:')
        for b in best.candidate:
            print(points[b.element[0]])
        print(points[best.candidate[-1].element[1]])
        print('Distance: {0}'.format(1/best.fitness))
    return ac

if __name__ == '__main__':
    main(display=True)