import networkx as nx


class TSP:
    def __init__(self, graph: nx.Graph, cutoff_time: int = 60):
        self.graph = graph
        self.distance_matrix = nx.to_numpy_array(graph)
        self.n = len(self.distance_matrix)
        self.cutoff_time = cutoff_time

        self.trace = []

    def update(self, route, distance, time, kwargs):
        self.trace.append({
            'route': route,
            'distance': distance,
            'time': time,
            **kwargs
        })

    def solve(self):
        raise NotImplementedError
