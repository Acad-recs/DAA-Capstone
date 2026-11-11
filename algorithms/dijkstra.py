"""Dijkstra's Single-Source Shortest Path Algorithm.

Complexity:
- Time Complexity: O((V + E) log V) using a min-heap priority queue (heapq).
- Space Complexity: O(V + E) to store the graph, distance map, predecessor map, and min-heap.
Where V is the number of vertices and E is the number of directed edges.

Properties:
- Non-negative edge weights only (raises ValueError on negative edges).
- Handles disconnected/unreachable nodes cleanly (distance remains float('inf'), path is empty).
- Reconstructs exact node-by-node path from source to target.
"""

import heapq
from typing import Dict, List, Optional, Tuple


def shortest_paths(
    graph: Dict[str, Dict[str, float]],
    source: str,
) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
    """Calculate shortest path distances and predecessor tree from *source* using Dijkstra's algorithm.

    Args:
        graph: Weighted adjacency list {node: {neighbor: weight, ...}, ...}
        source: Starting vertex identifier.

    Returns:
        A tuple of (distances, previous):
            - distances: Dict mapping each node to shortest distance from source.
            - previous: Dict mapping each node to its predecessor on the shortest path.

    Raises:
        KeyError: If source vertex is not present in graph.
        ValueError: If any edge weight is negative.
    """
    if source not in graph:
        raise KeyError(f"Source vertex '{source}' is not present in graph.")

    distances: Dict[str, float] = {node: float("inf") for node in graph}
    previous: Dict[str, Optional[str]] = {node: None for node in graph}
    distances[source] = 0.0

    # Priority queue stores tuples of (current_distance, node)
    pq: List[Tuple[float, str]] = [(0.0, source)]

    while pq:
        curr_dist, u = heapq.heappop(pq)

        # Lazy deletion / stale entry check in priority queue
        if curr_dist > distances[u]:
            continue

        for v, weight in graph.get(u, {}).items():
            if weight < 0:
                raise ValueError(
                    f"Dijkstra's algorithm does not support negative edge weights: "
                    f"edge ({u} -> {v}) has weight {weight}."
                )

            alt = curr_dist + weight
            if alt < distances.get(v, float("inf")):
                distances[v] = alt
                previous[v] = u
                heapq.heappush(pq, (alt, v))

    return distances, previous


def reconstruct_path(
    previous: Dict[str, Optional[str]],
    source: str,
    target: str,
) -> List[str]:
    """Reconstruct the sequence of vertices on the shortest path from *source* to *target*.

    Args:
        previous: Predecessor map returned by `shortest_paths`.
        source: Starting vertex identifier.
        target: Target destination vertex identifier.

    Returns:
        List of vertices [source, ..., target], or empty list if target is unreachable.
    """
    if source == target:
        return [source]

    path: List[str] = []
    curr: Optional[str] = target

    while curr is not None:
        path.append(curr)
        if curr == source:
            path.reverse()
            return path
        curr = previous.get(curr)

    return []  # Unreachable


def all_pairs_shortest_paths(
    graph: Dict[str, Dict[str, float]],
    nodes: Optional[List[str]] = None,
) -> Dict[str, Dict[str, float]]:
    """Compute pairwise shortest distances between all or a subset of nodes using repeated Dijkstra.

    Time Complexity: O(k * (V + E) log V) where k is the number of source vertices evaluated.
    """
    target_nodes = nodes if nodes is not None else list(graph.keys())
    dist_matrix: Dict[str, Dict[str, float]] = {}

    for src in target_nodes:
        if src in graph:
            dists, _ = shortest_paths(graph, src)
            dist_matrix[src] = {dst: dists.get(dst, float("inf")) for dst in target_nodes}

    return dist_matrix
