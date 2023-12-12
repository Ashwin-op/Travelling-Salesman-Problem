import os

import networkx as nx
import numpy as np

from tsp.branch_and_bound import BranchAndBound
from tsp.stochastic_local_search import StochasticLocalSearch


def run_searches(graph):
    print('Branch and Bound')
    tsp = BranchAndBound(graph)
    tsp.solve()
    print(tsp.trace[-1])

    print('Stochastic Local Search')
    tsp = StochasticLocalSearch(graph)
    tsp.solve()
    print(tsp.trace[-1])


if __name__ == "__main__":
    for file in os.listdir('competition'):
        if file.endswith('.txt') and file.startswith('tsp-problem-1000-400000-100-25-1'):
            print(file)
            matrix = np.loadtxt('competition/' + file, skiprows=1)
            run_searches(nx.from_numpy_array(matrix))
