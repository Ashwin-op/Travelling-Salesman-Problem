from time import time

from tsp.graph import TSP
from tsplib import load


def run_searches(graph):
    values = {}
    for i in range(10):
        tsp2 = TSP(graph)
        start = time()
        two_opt = tsp2.branch_and_bound()
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
    # problem = load('tests/a280.tsp/a280.tsp')
    # problem = load('tests/att48.tsp/att48.tsp')
    # problem = load('tests/bayg29.tsp/bayg29.tsp')
    # problem = load('tests/bays29.tsp/bays29.tsp')
    # problem = load('tests/berlin52.tsp/berlin52.tsp')
    # problem = load('tests/brazil58.tsp/brazil58.tsp')
    # problem = load('tests/burma14.tsp/burma14.tsp')
    # problem = load('tests/dantzig42.tsp/dantzig42.tsp')
    # problem = load('tests/eil51.tsp/eil51.tsp')
    # problem = load('tests/eil76.tsp/eil76.tsp')
    # problem = load('tests/usa13509.tsp/usa13509.tsp')
    problem = load('tests/ulysses16.tsp/ulysses16.tsp')
    # problem = load('tests/ulysses22.tsp/ulysses22.tsp')

    run_searches(problem.get_graph())
