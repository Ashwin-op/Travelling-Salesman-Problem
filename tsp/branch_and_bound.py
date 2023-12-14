from heapq import heappush, heappop
from time import time

from tsp.base import TSP


class Path:
    def __init__(self, distance_matrix, n, path, lower_bound_method):
        self.distance_matrix = distance_matrix
        self.n = n
        self.path = path

        if self.is_solution():
            self.lower_bound = None
        elif lower_bound_method == "MST":
            # Prim's algorithm
            root = None
            # Priority queue
            pq = []
            # Cost to add a vertex to the tree
            cost = {}
            mst_cost = 0
            for v in range(n):
                if root is None and v not in path:
                    root = v
                elif root is not None and v not in path:
                    cost[v] = distance_matrix[root][v]
                    heappush(pq, (distance_matrix[root][v], v))
            tree = {root} if root is not None else None
            while pq:
                (weight, v) = heappop(pq)
                if v not in tree:
                    mst_cost += weight
                    tree.add(v)
                    for u in range(n):
                        if u not in path and u not in tree and cost[u] > distance_matrix[v][u]:
                            cost[u] = distance_matrix[v][u]
                            heappush(pq, (distance_matrix[v][u], u))

            # Calculate a lower bound of any solution derived from this configuration:
            #   cost of the path +
            #   cost of the minimum spanning tree covering the vertices that are not in the path +
            #   minimum cost of joining the path ends to that minimum spanning tree
            self.lower_bound = self.get_path_cost() + mst_cost + \
                               min([distance_matrix[path[0]][v] for v in range(n) if v not in path]) if len(
                path) > 0 else 0 + \
                               min([distance_matrix[path[-1]][v] for v in range(n) if v not in path]) if len(
                path) > 1 else 0
        else:
            raise NotImplementedError

    def __lt__(self, other):
        # Prioritize depth.
        return (self.lower_bound / len(self.path)) < (other.get_lower_bound() / len(other.get_path()))
        # Prioritize breadth.
        # return self.lower_bound < other.get_lower_bound()

    def expand(self, v):
        if v in self.path:
            raise ValueError
        return Path(self.distance_matrix, self.n, self.path + [v], "MST")

    def is_solution(self):
        return len(self.path) == self.n

    def get_path_cost(self):
        return sum([self.distance_matrix[self.path[i]][self.path[i + 1]] for i in range(len(self.path) - 1)])

    def get_cycle_cost(self):
        return self.get_path_cost() + self.distance_matrix[self.path[-1]][self.path[0]]

    def get_lower_bound(self):
        return self.lower_bound

    def get_path(self):
        return self.path


class BranchAndBound(TSP):
    def solve(self):
        # Use a trivial tour (1-2-3-...-N-1) to set the global upper bound.
        tour = list(range(self.n))
        upper_bound = sum([self.distance_matrix[i][(i + 1) % self.n] for i in range(self.n)])

        frontier = [Path(self.distance_matrix, self.n, [0], "MST")]
        backtracks = 0  # Initialize backtracks counter
        total_branches = 0  # Initialize total branches counter
        levels = 0  # Initialize levels counter

        start_time = time()

        while frontier and (time() - start_time) < self.cutoff_time:
            config = heappop(frontier)
            branches = 0  # Counter for branches at this level

            for v in range(self.n):
                try:
                    expanded_config = config.expand(v)
                    branches += 1  # Increment branches count for each valid expansion
                except ValueError:
                    backtracks += 1  # Increment backtracks count on dead-end
                    continue

                if expanded_config.is_solution():
                    this_solution = expanded_config.get_cycle_cost()
                    if this_solution < upper_bound:
                        tour = list(expanded_config.get_path())
                        upper_bound = this_solution
                        self.update(tour + [0], this_solution, time() - start_time, {
                            "backtracks": backtracks,
                            "average_branching_factor": total_branches / levels
                        })
                elif expanded_config.get_lower_bound() < upper_bound:
                    heappush(frontier, expanded_config)

            if branches > 0:
                total_branches += branches
                levels += 1
