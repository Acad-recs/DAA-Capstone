"""Nearest Neighbor heuristic approximation for Travelling Salesperson Problem (TSP).

Workflow:
1. Start courier delivery tour at the depot.
2. Select the nearest unvisited delivery location based on shortest paths.
3. Advance to that location and mark it visited.
4. Repeat until all requested delivery stops are visited.
5. Return from the last stop back to the depot if a valid path exists.
6. Return both the delivery stop sequence and the fully expanded node-by-node travel path.

Complexity:
- Time Complexity: O(k^2) where k is the number of delivery locations to visit,
  using a precomputed shortest-path distance matrix.
- Space Complexity: O(k^2) for the distance matrix and O(V) for the expanded path.

Approximation Note:
- Nearest Neighbor is a greedy heuristic algorithm.
- It does NOT guarantee the optimal TSP tour, but yields a fast polynomial-time approximation.
"""

from typing import Dict, List, Optional, Set, Tuple

from algorithms.dijkstra import reconstruct_path, shortest_paths


def nearest_neighbor_tsp(
    graph: Dict[str, Dict[str, float]],
    depot: str,
    destinations: List[str],
) -> Tuple[List[str], List[str], float, List[str]]:
    """Solve delivery routing using the Nearest Neighbor heuristic over shortest paths.

    Args:
        graph: Weighted adjacency list representing the road network.
        depot: Origin location identifier (must exist in graph).
        destinations: List of delivery destination location IDs (may contain duplicates).

    Returns:
        A tuple of:
            - stop_sequence: Ordered sequence of delivery stops [depot, stop1, ..., depot].
            - expanded_path: Complete node-by-node physical travel path traversed.
            - total_distance: Total distance traveled across the entire tour.
            - unreachable: List of requested destinations that could not be reached from depot.
    """
    if depot not in graph:
        raise KeyError(f"Depot location '{depot}' not found in delivery graph.")

    # Remove duplicates while preserving deterministic order, and exclude depot from stops
    unique_stops: List[str] = []
    seen: Set[str] = set()
    for dest in destinations:
        if dest != depot and dest not in seen:
            seen.add(dest)
            unique_stops.append(dest)

    if not unique_stops:
        # No delivery stops requested
        return [depot], [depot], 0.0, []

    # Check reachability from depot
    depot_dists, _ = shortest_paths(graph, depot)
    reachable_stops: List[str] = []
    unreachable_stops: List[str] = []

    for stop in unique_stops:
        if stop in graph and depot_dists.get(stop, float("inf")) < float("inf"):
            reachable_stops.append(stop)
        else:
            unreachable_stops.append(stop)

    if not reachable_stops:
        return [depot], [depot], 0.0, unreachable_stops

    # Precompute all-pairs shortest paths and previous pointers for reachable nodes + depot
    nodes_of_interest = [depot] + reachable_stops
    distance_matrix: Dict[str, Dict[str, float]] = {}
    predecessor_matrix: Dict[str, Dict[str, Optional[str]]] = {}

    for u in nodes_of_interest:
        dists, prev = shortest_paths(graph, u)
        distance_matrix[u] = dists
        predecessor_matrix[u] = prev

    # Nearest Neighbor Greedy Walk
    current_node = depot
    unvisited: Set[str] = set(reachable_stops)
    stop_sequence: List[str] = [depot]
    expanded_path: List[str] = [depot]
    total_distance = 0.0

    while unvisited:
        # Find nearest unvisited destination from current_node
        next_node = None
        min_distance = float("inf")

        # Sort candidate list for deterministic tie-breaking
        for candidate in sorted(unvisited):
            cand_dist = distance_matrix[current_node].get(candidate, float("inf"))
            if cand_dist < min_distance:
                min_distance = cand_dist
                next_node = candidate

        if next_node is None or min_distance == float("inf"):
            # Remaining stops cannot be reached from current_node
            unreachable_stops.extend(sorted(unvisited))
            break

        # Append segment to expanded path
        segment = reconstruct_path(
            predecessor_matrix[current_node],
            current_node,
            next_node,
        )
        if segment and len(segment) > 1:
            expanded_path.extend(segment[1:])
        elif not segment and current_node != next_node:
            # Fallback if no path found
            expanded_path.append(next_node)

        total_distance += min_distance
        stop_sequence.append(next_node)
        unvisited.remove(next_node)
        current_node = next_node

    # Return to depot from last stop
    return_dist = distance_matrix[current_node].get(depot, float("inf"))
    if return_dist < float("inf"):
        return_segment = reconstruct_path(
            predecessor_matrix[current_node],
            current_node,
            depot,
        )
        if return_segment and len(return_segment) > 1:
            expanded_path.extend(return_segment[1:])
        stop_sequence.append(depot)
        total_distance += return_dist
    else:
        # Cannot return to depot
        pass

    return stop_sequence, expanded_path, total_distance, unreachable_stops


def nearest_route(
    graph: Dict[str, Dict[str, float]],
    start: str,
) -> Tuple[List[str], float]:
    """Backward-compatible wrapper for TSP tour over all other nodes in graph."""
    other_nodes = [node for node in graph if node != start]
    stops, _, dist, _ = nearest_neighbor_tsp(graph, start, other_nodes)
    return stops, dist
