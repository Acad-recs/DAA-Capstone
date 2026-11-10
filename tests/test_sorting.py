import unittest

from algorithms.sorting import merge_sort


class SortingTests(unittest.TestCase):
    def test_merge_sort(self):
        self.assertEqual(merge_sort([3, 1, 2]), [1, 2, 3])
