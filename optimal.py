import os

import numpy as np
import pandas as pd
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

ROUND = 10e6


def create_data_model(file_name):
    """Stores the data for the problem."""
    return {"distance_matrix": (np.loadtxt(file_name, skiprows=1) * ROUND).astype(int), "num_vehicles": 1, "depot": 0}


def print_solution(manager, routing, solution):
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue() / ROUND} miles")
    index = routing.Start(0)
    plan_output = "Route for vehicle 0:\n"
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += f" {manager.IndexToNode(index)} ->"
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += f" {manager.IndexToNode(index)}\n"
    print(plan_output)
    plan_output += f"Route distance: {route_distance}miles\n"


def main(file_name):
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model(file_name)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.AUTOMATIC
    )

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(manager, routing, solution)

    return manager, routing, solution


if __name__ == "__main__":
    results = pd.DataFrame(columns=["file", "path", "cost"])
    for file in os.listdir("competition"):
        if file.endswith(".txt") and file.startswith("tsp-problem-"):
            print(file)
            manager, routing, solution = main("competition/" + file)
            index = routing.Start(0)
            path = []
            while not routing.IsEnd(index):
                path.append(manager.IndexToNode(index))
                index = solution.Value(routing.NextVar(index))
            path.append(manager.IndexToNode(index))
            results = pd.concat([results, pd.DataFrame([[file, path, solution.ObjectiveValue() / ROUND]],
                                                       columns=["file", "path", "cost"])])

    results = results.sort_values(by=["file"])
    results.to_csv("optimal_results.csv", index=False)
