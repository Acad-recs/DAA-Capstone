import unittest

from algorithms.tsp import nearest_route


class TspTests(unittest.TestCase):
    def test_returns_cycle(self):
        graph = {"A": {"B": 1, "C": 2}, "B": {"A": 1, "C": 1},
                 "C": {"A": 2, "B": 1}}
        route, cost = nearest_route(graph, "A")
        self.assertEqual(route[0], "A")
        self.assertEqual(route[-1], "A")
        self.assertEqual(cost, 4)
