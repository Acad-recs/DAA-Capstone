"""Dijkstra shortest-path algorithm."""

import heapq


def shortest_paths(graph, source):
    """Return shortest distances and predecessor information."""
    distances = {node: float("inf") for node in graph}
    previous = {node: None for node in graph}
    distances[source] = 0
    queue = [(0, source)]

    while queue:
        distance, node = heapq.heappop(queue)
        if distance != distances[node]:
            continue
        for neighbor, weight in graph.get(node, {}).items():
            if weight < 0:
                raise ValueError("Dijkstra requires non-negative edge weights")
            candidate = distance + weight
            if candidate < distances.get(neighbor, float("inf")):
                distances[neighbor] = candidate
                previous[neighbor] = node
                heapq.heappush(queue, (candidate, neighbor))
    return distances, previous


def reconstruct_path(previous, source, target):
    """Reconstruct a path from predecessor data."""
    path = []
    current = target
    while current is not None:
        path.append(current)
        if current == source:
            return list(reversed(path))
        current = previous.get(current)
    return []
