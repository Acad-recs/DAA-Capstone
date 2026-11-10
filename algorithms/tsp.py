"""Small travelling salesperson solver using permutation search."""

from itertools import permutations


def nearest_route(graph, start):
    """Return the shortest Hamiltonian cycle found by brute force."""
    locations = [node for node in graph if node != start]
    best_route = None
    best_cost = float("inf")
    for ordering in permutations(locations):
        route = (start,) + ordering + (start,)
        cost = sum(graph[route[index]][route[index + 1]]
                   for index in range(len(route) - 1))
        if cost < best_cost:
            best_route, best_cost = route, cost
    return list(best_route or [start]), best_cost
