"""Delivery location graph loading, representation, validation, and operations."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from algorithms.dijkstra import all_pairs_shortest_paths, reconstruct_path, shortest_paths


class GraphManager:
    """Manages weighted adjacency-list representation of delivery locations."""

    def __init__(self, data_path: Optional[Path] = None, graph: Optional[Dict[str, Dict[str, float]]] = None):
        """Initialize GraphManager from file path or existing adjacency list."""
        self.data_path = Path(data_path) if data_path else None
        if graph is not None:
            self.graph = self.validate_graph(graph)
        elif self.data_path is not None:
            self.graph = self._load()
        else:
            self.graph = {}

    def _load(self) -> Dict[str, Dict[str, float]]:
        """Load and validate delivery locations graph from JSON."""
        if not self.data_path.exists():
            raise FileNotFoundError(f"Location graph file not found: {self.data_path}")
        with self.data_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, dict):
            raise ValueError("Graph dataset must be a JSON object mapping location names to neighbor distances.")
        return self.validate_graph(data)

    @classmethod
    def validate_graph(cls, graph: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
        """Validate weighted adjacency-list graph structure.

        Ensures:
        - Graph is non-empty dictionary.
        - Node names are non-empty strings.
        - Neighbors are dictionaries with numeric, non-negative weights.
        - Referenced neighbor nodes exist as keys in the graph.
        """
        if not isinstance(graph, dict):
            raise ValueError("Graph must be a dictionary representing an adjacency list.")

        validated: Dict[str, Dict[str, float]] = {}
        all_nodes = set(graph.keys())

        for node, neighbors in graph.items():
            if not isinstance(node, str) or not node.strip():
                raise ValueError("Graph node identifiers must be non-empty strings.")
            if not isinstance(neighbors, dict):
                raise ValueError(f"Neighbors for node '{node}' must be a dictionary of {{neighbor: weight}}.")

            validated_neighbors: Dict[str, float] = {}
            for neighbor, weight in neighbors.items():
                if not isinstance(neighbor, str) or not neighbor.strip():
                    raise ValueError(f"Neighbor identifier from '{node}' must be a non-empty string.")
                if neighbor not in all_nodes:
                    raise ValueError(f"Neighbor '{neighbor}' of node '{node}' is not declared in graph nodes.")
                if not isinstance(weight, (int, float)):
                    raise ValueError(f"Edge weight between '{node}' and '{neighbor}' must be numeric.")
                if weight < 0:
                    raise ValueError(f"Edge weight between '{node}' and '{neighbor}' cannot be negative: {weight}.")

                validated_neighbors[neighbor] = float(weight)

            validated[node] = validated_neighbors

        return validated

    def nodes(self) -> List[str]:
        """Return list of all location IDs/names in the graph."""
        return list(self.graph.keys())

    def get_neighbors(self, node: str) -> Dict[str, float]:
        """Return adjacency dictionary for a given node."""
        if node not in self.graph:
            raise KeyError(f"Location '{node}' does not exist in graph.")
        return self.graph[node]

    def route(self, source: str, target: str) -> Tuple[List[str], float]:
        """Find the shortest path and distance from source to target using Dijkstra."""
        if source not in self.graph:
            raise KeyError(f"Source location '{source}' not in graph.")
        if target not in self.graph:
            raise KeyError(f"Target location '{target}' not in graph.")

        distances, previous = shortest_paths(self.graph, source)
        path = reconstruct_path(previous, source, target)
        return path, distances[target]

    def all_shortest_distances(self, subset_nodes: Optional[List[str]] = None) -> Dict[str, Dict[str, float]]:
        """Calculate pairwise shortest-path distances across all or subset of nodes."""
        nodes_to_compute = subset_nodes or self.nodes()
        return all_pairs_shortest_paths(self.graph, nodes_to_compute)
