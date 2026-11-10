import unittest

from algorithms.dijkstra import reconstruct_path, shortest_paths


class DijkstraTests(unittest.TestCase):
    def test_shortest_path(self):
        graph = {"A": {"B": 2}, "B": {"C": 3}, "C": {}}
        distances, previous = shortest_paths(graph, "A")
        self.assertEqual(distances["C"], 5)
        self.assertEqual(reconstruct_path(previous, "A", "C"), ["A", "B", "C"])
