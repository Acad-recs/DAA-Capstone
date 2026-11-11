"""Unit tests for Nearest Neighbor TSP approximation algorithm."""

import unittest

from algorithms.tsp import nearest_neighbor_tsp, nearest_route


class TestTsp(unittest.TestCase):
    """Test suite for nearest neighbor route generation and edge case handling."""

    def setUp(self):
        # A simple triangle: Depot, A, B
        self.triangle_graph = {
            "Depot": {"A": 3.0, "B": 10.0},
            "A": {"Depot": 3.0, "B": 4.0},
            "B": {"Depot": 10.0, "A": 4.0},
        }

    def test_single_delivery_location(self):
        stops, path, dist, unreachable = nearest_neighbor_tsp(
            self.triangle_graph, "Depot", ["A"]
        )
        self.assertEqual(stops, ["Depot", "A", "Depot"])
        self.assertEqual(path, ["Depot", "A", "Depot"])
        self.assertEqual(dist, 6.0)  # 3 + 3
        self.assertEqual(unreachable, [])

    def test_multiple_destinations_nearest_neighbor_ordering(self):
        # From Depot: A is dist 3, B is dist 7 (via A).
        # Nearest is A (dist 3).
        # From A: B is dist 4.
        # From B: Return to Depot is dist 7 (via A: B -> A -> Depot = 4 + 3 = 7).
        # Total distance = 3 + 4 + 7 = 14.
        stops, path, dist, unreachable = nearest_neighbor_tsp(
            self.triangle_graph, "Depot", ["B", "A"]
        )
        self.assertEqual(stops, ["Depot", "A", "B", "Depot"])
        self.assertEqual(path, ["Depot", "A", "B", "A", "Depot"])
        self.assertEqual(dist, 14.0)
        self.assertEqual(unreachable, [])

    def test_duplicate_destinations_handled_without_duplicate_stops(self):
        stops, path, dist, unreachable = nearest_neighbor_tsp(
            self.triangle_graph, "Depot", ["A", "A", "B", "A"]
        )
        # Unique destinations are A and B
        self.assertEqual(stops, ["Depot", "A", "B", "Depot"])
        self.assertEqual(dist, 14.0)

    def test_empty_destinations(self):
        stops, path, dist, unreachable = nearest_neighbor_tsp(
            self.triangle_graph, "Depot", []
        )
        self.assertEqual(stops, ["Depot"])
        self.assertEqual(dist, 0.0)

    def test_disconnected_destination_reported(self):
        disconnected_graph = {
            "Depot": {"A": 2.0},
            "A": {"Depot": 2.0},
            "Island": {},
        }
        stops, path, dist, unreachable = nearest_neighbor_tsp(
            disconnected_graph, "Depot", ["A", "Island"]
        )
        self.assertEqual(stops, ["Depot", "A", "Depot"])
        self.assertEqual(unreachable, ["Island"])

    def test_expanded_path_with_intermediate_nodes(self):
        # Depot -> X -> Y. Destination is only Y.
        linear_graph = {
            "Depot": {"X": 2.0},
            "X": {"Depot": 2.0, "Y": 3.0},
            "Y": {"X": 3.0},
        }
        stops, path, dist, unreachable = nearest_neighbor_tsp(
            linear_graph, "Depot", ["Y"]
        )
        self.assertEqual(stops, ["Depot", "Y", "Depot"])
        self.assertEqual(path, ["Depot", "X", "Y", "X", "Depot"])
        self.assertEqual(dist, 10.0)  # 2 + 3 + 3 + 2

    def test_backward_compatibility_nearest_route(self):
        route, cost = nearest_route(self.triangle_graph, "Depot")
        self.assertEqual(route[0], "Depot")
        self.assertEqual(route[-1], "Depot")
        self.assertEqual(cost, 14.0)


if __name__ == "__main__":
    unittest.main()
