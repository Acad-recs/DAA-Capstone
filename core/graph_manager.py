"""Location graph loading and shortest-route services."""

import json
from pathlib import Path

from algorithms.dijkstra import reconstruct_path, shortest_paths


class GraphManager:
    """Load a weighted location graph."""

    def __init__(self, data_path):
        self.data_path = Path(data_path)
        self.graph = self._load()

    def _load(self):
        with self.data_path.open(encoding="utf-8") as file:
            return json.load(file)

    def route(self, source, target):
        distances, previous = shortest_paths(self.graph, source)
        return reconstruct_path(previous, source, target), distances[target]
