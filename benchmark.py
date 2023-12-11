from time import time

import networkx as nx
import numpy as np

from tsp.graph import TSP


def run_searches(graph):
    values = {}
    for i in range(1):
        tsp2 = TSP(graph)
        start = time()
        two_opt = tsp2.two_opt()
        end = time()

        values[i] = {
            'solution': two_opt,
            'time': end - start
        }

    best_solution = min(values.values(), key=lambda x: x['solution'][1])
    print(f'Best path: {best_solution["solution"][0]}')
    print(f'Cost: {best_solution["solution"][1]}')
    print(f'Time (seconds): {best_solution["time"]}')


if __name__ == "__main__":
    matrix = np.loadtxt('competition/tsp-problem-1000-400000-100-25-1.txt', skiprows=1)
    run_searches(nx.from_numpy_array(matrix))
