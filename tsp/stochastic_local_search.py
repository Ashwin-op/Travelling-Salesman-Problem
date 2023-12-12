from random import sample
from time import time

from tsp.base import TSP


class StochasticLocalSearch(TSP):
    @staticmethod
    def calculate_path_dist(distance_matrix, path):
        return sum(distance_matrix[path[ind]][path[ind + 1]] for ind in range(len(path) - 1))

    @staticmethod
    def swap(path, swap_first, swap_last):
        return path[0:swap_first] + path[swap_last:-len(path) + swap_first - 1:-1] + path[swap_last + 1:len(path)]

    def solve(self, improvement_threshold=0.01):
        tour = [0] + sample(range(1, self.n), self.n - 1) + [0]
        upper_bound = self.calculate_path_dist(self.distance_matrix, tour)

        start_time = time()

        improvement_factor = 1
        while improvement_factor > improvement_threshold and time() - start_time < self.cutoff_time:
            previous_best = upper_bound
            for swap_first in range(1, self.n - 2):
                for swap_last in range(swap_first + 1, self.n - 1):
                    before_start = tour[swap_first - 1]
                    start = tour[swap_first]
                    end = tour[swap_last]
                    after_end = tour[swap_last + 1]
                    before = self.distance_matrix[before_start][start] + self.distance_matrix[end][after_end]
                    after = self.distance_matrix[before_start][end] + self.distance_matrix[start][after_end]
                    if after < before:
                        tour = self.swap(tour, swap_first, swap_last)
                        upper_bound = self.calculate_path_dist(self.distance_matrix, tour)
                        self.update(tour, upper_bound, time() - start_time, {})
            improvement_factor = 1 - upper_bound / previous_best
