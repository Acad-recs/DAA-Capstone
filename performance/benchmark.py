"""Basic performance benchmark entry point."""

from time import perf_counter

from algorithms.sorting import merge_sort


def benchmark_sort(values):
    start = perf_counter()
    merge_sort(values)
    return perf_counter() - start
