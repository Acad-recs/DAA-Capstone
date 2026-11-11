"""Unit tests for 0/1 Knapsack dynamic programming algorithm and parcel selection."""

import unittest

from algorithms.knapsack import knapsack, knapsack_01


class TestKnapsack(unittest.TestCase):
    """Test suite for knapsack DP table construction, item selection, and edge cases."""

    def test_empty_items(self):
        selected, rejected, total_w, total_v, table = knapsack_01([], capacity=10)
        self.assertEqual(selected, [])
        self.assertEqual(rejected, [])
        self.assertEqual(total_w, 0)
        self.assertEqual(total_v, 0)
        self.assertEqual(table, [[0] * 11])

    def test_zero_capacity(self):
        items = [{"id": 1, "weight": 5, "value": 10}]
        selected, rejected, total_w, total_v, _ = knapsack_01(items, capacity=0)
        self.assertEqual(selected, [])
        self.assertEqual(rejected, items)
        self.assertEqual(total_w, 0)
        self.assertEqual(total_v, 0)

    def test_negative_capacity_raises_error(self):
        with self.assertRaises(ValueError):
            knapsack_01([], capacity=-5)

    def test_item_heavier_than_capacity(self):
        items = [
            {"id": "A", "weight": 10, "value": 50},
            {"id": "B", "weight": 3, "value": 30},
        ]
        selected, rejected, total_w, total_v, _ = knapsack_01(items, capacity=5)
        self.assertEqual(selected, [{"id": "B", "weight": 3, "value": 30}])
        self.assertEqual(rejected, [{"id": "A", "weight": 10, "value": 50}])
        self.assertEqual(total_w, 3)
        self.assertEqual(total_v, 30)

    def test_exact_capacity_match(self):
        items = [
            {"id": 1, "weight": 2, "value": 20},
            {"id": 2, "weight": 3, "value": 30},
        ]
        selected, rejected, total_w, total_v, _ = knapsack_01(items, capacity=5)
        self.assertEqual(total_w, 5)
        self.assertEqual(total_v, 50)
        self.assertEqual(len(selected), 2)
        self.assertEqual(len(rejected), 0)

    def test_optimal_tradeoff_better_than_greedy(self):
        # Greedy by value/weight ratio would pick item 1 (ratio 6/1 = 6) and item 2 (ratio 10/2 = 5)
        # Total value = 16 for weight 3.
        # But optimal for capacity 5 is item 2 (w=2, v=10) and item 3 (w=3, v=18) -> total value = 28, weight = 5.
        items = [
            {"id": 1, "weight": 1, "value": 6},   # ratio 6.0
            {"id": 2, "weight": 2, "value": 10},  # ratio 5.0
            {"id": 3, "weight": 3, "value": 18},  # ratio 6.0
            {"id": 4, "weight": 5, "value": 25},  # ratio 5.0
        ]
        selected, rejected, total_w, total_v, _ = knapsack_01(items, capacity=5)
        self.assertEqual(total_v, 28)
        self.assertEqual(total_w, 5)
        selected_ids = [item["id"] for item in selected]
        self.assertEqual(selected_ids, [2, 3])

    def test_backward_compatibility_wrapper(self):
        items = [{"weight": 2, "value": 15}, {"weight": 3, "value": 20}]
        selected, val = knapsack(items, 4)
        self.assertEqual(val, 20)
        self.assertEqual(selected, [{"weight": 3, "value": 20}])

    def test_dp_table_dimensions(self):
        items = [
            {"weight": 2, "value": 10},
            {"weight": 3, "value": 20},
            {"weight": 4, "value": 30},
        ]
        _, _, _, _, table = knapsack_01(items, capacity=7)
        # Dimensions must be (n + 1) x (W + 1) -> 4 rows x 8 columns
        self.assertEqual(len(table), 4)
        for row in table:
            self.assertEqual(len(row), 8)


if __name__ == "__main__":
    unittest.main()
