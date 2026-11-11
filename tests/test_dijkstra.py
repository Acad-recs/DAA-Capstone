"""Unit tests for Dijkstra shortest path algorithm and edge case validation."""

import unittest

from algorithms.dijkstra import all_pairs_shortest_paths, reconstruct_path, shortest_paths


class TestDijkstra(unittest.TestCase):
    """Test suite covering Dijkstra shortest paths, path reconstruction, and error conditions."""

    def setUp(self):
        # Standard weighted graph
        self.graph = {
            "Depot": {"A": 2.0, "B": 5.0},
            "A": {"Depot": 2.0, "B": 1.0, "C": 7.0},
            "B": {"Depot": 5.0, "A": 1.0, "C": 2.0, "D": 4.0},
            "C": {"A": 7.0, "B": 2.0, "D": 1.0},
            "D": {"B": 4.0, "C": 1.0},
        }

    def test_shortest_path_standard(self):
        distances, previous = shortest_paths(self.graph, "Depot")
        # Depot -> A = 2
        self.assertEqual(distances["A"], 2.0)
        # Depot -> A -> B = 3 (better than direct 5)
        self.assertEqual(distances["B"], 3.0)
        # Depot -> A -> B -> C = 5
        self.assertEqual(distances["C"], 5.0)
        # Depot -> A -> B -> C -> D = 6
        self.assertEqual(distances["D"], 6.0)

        path_to_d = reconstruct_path(previous, "Depot", "D")
        self.assertEqual(path_to_d, ["Depot", "A", "B", "C", "D"])

    def test_source_equals_destination(self):
        distances, previous = shortest_paths(self.graph, "Depot")
        self.assertEqual(distances["Depot"], 0.0)
        path = reconstruct_path(previous, "Depot", "Depot")
        self.assertEqual(path, ["Depot"])

    def test_invalid_source_raises_key_error(self):
        with self.assertRaises(KeyError):
            shortest_paths(self.graph, "NonExistentLocation")

    def test_negative_edge_weight_raises_value_error(self):
        invalid_graph = {
            "A": {"B": -3.0},
            "B": {"A": 2.0},
        }
        with self.assertRaises(ValueError):
            shortest_paths(invalid_graph, "A")

    def test_disconnected_subgraph(self):
        disconnected_graph = {
            "A": {"B": 1.0},
            "B": {"A": 1.0},
            "C": {"D": 2.0},
            "D": {"C": 2.0},
        }
        distances, previous = shortest_paths(disconnected_graph, "A")
        self.assertEqual(distances["A"], 0.0)
        self.assertEqual(distances["B"], 1.0)
        self.assertEqual(distances["C"], float("inf"))
        self.assertEqual(distances["D"], float("inf"))

        self.assertEqual(reconstruct_path(previous, "A", "C"), [])

    def test_all_pairs_shortest_paths(self):
        matrix = all_pairs_shortest_paths(self.graph, ["Depot", "B", "D"])
        self.assertEqual(matrix["Depot"]["B"], 3.0)
        self.assertEqual(matrix["Depot"]["D"], 6.0)
        self.assertEqual(matrix["B"]["D"], 3.0)  # B -> C -> D = 2 + 1 = 3


if __name__ == "__main__":
    unittest.main()
