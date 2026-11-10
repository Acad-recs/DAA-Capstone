import unittest

from algorithms.knapsack import knapsack


class KnapsackTests(unittest.TestCase):
    def test_selects_highest_value_combination(self):
        items = [{"weight": 2, "priority": 5}, {"weight": 3, "priority": 8}]
        selected, value = knapsack(items, 3)
        self.assertEqual(value, 8)
        self.assertEqual(selected, [items[1]])
