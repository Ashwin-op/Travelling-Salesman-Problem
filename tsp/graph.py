from itertools import permutations
from multiprocessing import Pool
from random import sample

import networkx as nx
import numpy as np


class TSP:
    def __init__(self, graph: nx.Graph):
        self.graph = graph

        self.distance_matrix = nx.to_numpy_array(graph)
        self.n = len(self.distance_matrix)
        self.best_route = []
        self.best_distance = 0
        self.distances = []

    def update(self, new_route, new_distance):
        self.best_distance = new_distance
        self.best_route = new_route
        return self.best_distance, self.best_route

    def exhaustive_search(self):
        self.best_route = [0] + list(range(1, self.n)) + [0]
        self.best_distance = self.calculate_path_dist(self.distance_matrix, self.best_route)

        # Create a pool of workers
        with Pool() as pool:
            # Use starmap to apply the calculate_path_dist function to each permutation
            results = pool.starmap(self.calculate_path_dist,
                                   [(self.distance_matrix, [0] + list(route) + [0]) for route in
                                    permutations(list(range(1, self.n)))])

        # Find the minimum distance and its corresponding route
        min_distance = min(results)
        min_route = [0] + list(list(permutations(list(range(1, self.n))))[results.index(min_distance)]) + [0]

        # Update the best route and distance
        self.update(min_route, min_distance)
        # self.distances = results

        return self.best_route, self.best_distance, self.distances

    @staticmethod
    def calculate_path_dist(distance_matrix, path):
        return sum(distance_matrix[path[ind]][path[ind + 1]] for ind in range(len(path) - 1))

    @staticmethod
    def swap(path, swap_first, swap_last):
        return path[0:swap_first] + path[swap_last:-len(path) + swap_first - 1:-1] + path[swap_last + 1:len(path)]

    def two_opt(self, improvement_threshold=0.01):
        self.best_route = [0] + sample(range(1, self.n), self.n - 1) + [0]
        self.best_distance = self.calculate_path_dist(self.distance_matrix, self.best_route)
        improvement_factor = 1

        while improvement_factor > improvement_threshold:
            previous_best = self.best_distance
            for swap_first in range(1, self.n - 2):
                for swap_last in range(swap_first + 1, self.n - 1):
                    before_start = self.best_route[swap_first - 1]
                    start = self.best_route[swap_first]
                    end = self.best_route[swap_last]
                    after_end = self.best_route[swap_last + 1]
                    before = self.distance_matrix[before_start][start] + self.distance_matrix[end][after_end]
                    after = self.distance_matrix[before_start][end] + self.distance_matrix[start][after_end]
                    if after < before:
                        new_route = self.swap(self.best_route, swap_first, swap_last)
                        new_distance = self.calculate_path_dist(self.distance_matrix, new_route)
                        self.update(new_route, new_distance)
                        self.distances.append(self.best_distance)

            improvement_factor = 1 - self.best_distance / previous_best
        return self.best_route, self.best_distance, self.distances

    def mst_cost(self, visited):
        unvisited = set(range(self.n)) - visited
        unvisited_matrix = self.distance_matrix[list(unvisited)][:, list(unvisited)]
        mst = nx.minimum_spanning_tree(nx.from_numpy_array(unvisited_matrix))
        return sum(mst[i][j]["weight"] for i, j in mst.edges())

    def branch_and_bound_helper(self, node, path, cost, visited):
        if len(path) == self.n:
            cost += self.distance_matrix[node][0]
            if cost < self.best_distance:
                self.update(path + [0], cost)
                self.distances.append(self.best_distance)
        else:
            for i in range(self.n):
                if i not in visited:
                    if cost + self.distance_matrix[node][i] + self.mst_cost(visited | {i}) < self.best_distance:
                        self.branch_and_bound_helper(i, path + [i], cost + self.distance_matrix[node][i], visited | {i})

    def branch_and_bound(self):
        initial_path = [0]
        self.best_distance = np.inf
        self.branch_and_bound_helper(initial_path[0], initial_path, 0, {0})
        return self.best_route, self.best_distance, self.distances


if __name__ == "__main__":
    matrix = np.array([
        [0, 2, 5, 8],
        [2, 0, 4, 1],
        [5, 4, 0, 3],
        [8, 1, 3, 0]
    ])
    G = nx.from_numpy_array(matrix)
    tsp = TSP(G)
    print(tsp.branch_and_bound())
