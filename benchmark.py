import os
from multiprocessing import Pool

import networkx as nx
import numpy as np
import pandas as pd

from tsp.branch_and_bound import BranchAndBound
from tsp.stochastic_local_search import StochasticLocalSearch


def run_branch_bound(matrix):
    tsp = BranchAndBound(matrix, 60)
    tsp.solve()

    return tsp.trace


def test_bb():
    results = []
    for file in os.listdir('competition'):
        if file.endswith('.txt') and (
                file.startswith('tsp-problem-25-') or file.startswith('tsp-problem-50-') or file.startswith(
            'tsp-problem-75-') or file.startswith('tsp-problem-100-') or file.startswith(
            'tsp-problem-200-') or file.startswith('tsp-problem-300-')):
            print(file)
            matrix = np.loadtxt('competition/' + file, skiprows=1)
            trace = run_branch_bound(nx.from_numpy_array(matrix))
            for i in range(len(trace)):
                results.append({
                    'file': file,
                    **trace[i],
                })

    results = pd.DataFrame(results)
    results = results.sort_values(by=['file'])
    results.to_csv('branch_and_bound_results.csv', index=False)


def run_sls(filename):
    matrix = np.loadtxt('competition/' + filename, skiprows=1)
    tsp = StochasticLocalSearch(nx.from_numpy_array(matrix), 600)
    tsp.solve()
    return {
        'file': filename,
        **tsp.trace[-1],
    }


def test_sls():
    # use multiprocessing to run the stochastic local search algorithm on multiple files at once
    # this is faster than running them sequentially
    filenames = [
        file for file in os.listdir('competition') if file.endswith('.txt') and file.startswith('tsp-problem-')
    ]

    # run the algorithm on each file 500 times and save each result to a csv file

    for i in range(500):
        print('iteration', i)
        with Pool() as pool:
            results = pool.map(run_sls, filenames)
        results = pd.DataFrame(results)
        results = results.sort_values(by=['file'])
        results.to_csv('sls/stochastic_local_search_results_' + str(i) + '.csv', index=False)


if __name__ == '__main__':
    # test_bb()
    test_sls()
