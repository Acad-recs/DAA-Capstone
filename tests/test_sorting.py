"""Unit tests for manual Merge Sort and parcel prioritization logic."""

import unittest

from algorithms.sorting import merge_sort, sort_parcels


class TestMergeSort(unittest.TestCase):
    """Test suite covering edge cases and correctness for Merge Sort."""

    def test_empty_list(self):
        self.assertEqual(merge_sort([]), [])

    def test_single_element(self):
        self.assertEqual(merge_sort([42]), [42])

    def test_already_sorted(self):
        self.assertEqual(merge_sort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

    def test_reverse_sorted(self):
        self.assertEqual(merge_sort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])

    def test_duplicates(self):
        self.assertEqual(merge_sort([3, 1, 3, 2, 1]), [1, 1, 2, 3, 3])

    def test_negative_numbers(self):
        self.assertEqual(merge_sort([-5, 10, -20, 0, 15]), [-20, -5, 0, 10, 15])

    def test_custom_key_and_reverse(self):
        words = ["apple", "banana", "kiwi", "fig"]
        # Sort by length descending
        sorted_words = merge_sort(words, key=len, reverse=True)
        self.assertEqual(sorted_words, ["banana", "apple", "kiwi", "fig"])

    def test_stability(self):
        # Stable sort must preserve original relative order for equal keys
        records = [
            {"id": "A", "val": 2},
            {"id": "B", "val": 1},
            {"id": "C", "val": 2},
            {"id": "D", "val": 1},
        ]
        sorted_records = merge_sort(records, key=lambda r: r["val"])
        ids = [r["id"] for r in sorted_records]
        self.assertEqual(ids, ["B", "D", "A", "C"])


class TestParcelPrioritization(unittest.TestCase):
    """Test suite for courier parcel ordering policy."""

    def test_empty_parcels(self):
        self.assertEqual(sort_parcels([]), [])

    def test_priority_first_then_deadline(self):
        parcels = [
            {"parcel_id": "P3", "priority": 2, "deadline": 10},
            {"parcel_id": "P1", "priority": 1, "deadline": 15},
            {"parcel_id": "P2", "priority": 1, "deadline": 10},
            {"parcel_id": "P4", "priority": 2, "deadline": 8},
        ]
        ordered = sort_parcels(parcels)
        ordered_ids = [p["parcel_id"] for p in ordered]
        # P2 has priority 1, deadline 10
        # P1 has priority 1, deadline 15
        # P4 has priority 2, deadline 8
        # P3 has priority 2, deadline 10
        self.assertEqual(ordered_ids, ["P2", "P1", "P4", "P3"])

    def test_duplicate_priority_and_deadline_tiebreaker(self):
        parcels = [
            {"parcel_id": "P_B", "priority": 1, "deadline": 10},
            {"parcel_id": "P_A", "priority": 1, "deadline": 10},
        ]
        ordered = sort_parcels(parcels)
        self.assertEqual([p["parcel_id"] for p in ordered], ["P_A", "P_B"])


if __name__ == "__main__":
    unittest.main()
