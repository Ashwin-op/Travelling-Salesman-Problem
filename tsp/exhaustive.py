from itertools import permutations
from multiprocessing import Pool

from tsp.base import TSP


class Exhaustive(TSP):
    @staticmethod
    def calculate_path_dist(distance_matrix, path):
        return sum(distance_matrix[path[i]][path[i + 1]] for i in range(len(path) - 1))

    def solve(self, improvement_threshold=0.01):
        tour = [0] + list(range(1, self.n)) + [0]
        upper_bound = self.calculate_path_dist(self.distance_matrix, tour)

        with Pool() as pool:
            results = pool.starmap(self.calculate_path_dist,
                                   [(self.distance_matrix, [0] + list(route) + [0]) for route in
                                    permutations(list(range(1, self.n)))])

        min_distance = min(results)
        min_route = [0] + list(list(permutations(list(range(1, self.n))))[results.index(min_distance)]) + [0]

        self.update(min_route, min_distance, 0, {})
        # self.distances = results
