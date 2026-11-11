"""Benchmarking framework for algorithm performance evaluation.

Measures actual execution times across varying input sizes:
- Merge Sort: n in [10, 100, 500, 1000, 2000, 5000]
- 0/1 Knapsack: n in [10, 50, 100, 200, 500], capacity = 100
- Dijkstra: graph vertices V in [10, 25, 50, 100, 200]
- Nearest Neighbor TSP: delivery locations in [5, 10, 15, 20, 25]

Uses time.perf_counter() for high-resolution timing.
"""

import random
import time
from typing import Any, Dict, List, Tuple

from algorithms.dijkstra import shortest_paths
from algorithms.knapsack import knapsack_01
from algorithms.sorting import merge_sort
from algorithms.tsp import nearest_neighbor_tsp


def generate_random_parcels(n: int, seed: int = 42) -> List[Dict[str, Any]]:
    """Generate synthetic parcel datasets for sorting and knapsack benchmarks."""
    rng = random.Random(seed + n)
    parcels = []
    for i in range(n):
        parcels.append({
            "parcel_id": f"P{i:05d}",
            "destination": f"Loc_{rng.randint(1, max(2, n // 5))}",
            "weight": rng.randint(1, 20),
            "value": rng.randint(10, 100),
            "priority": rng.randint(1, 5),
            "deadline": rng.randint(1, 100),
        })
    return parcels


def generate_random_connected_graph(num_nodes: int, edge_probability: float = 0.3, seed: int = 42) -> Dict[str, Dict[str, float]]:
    """Generate synthetic connected weighted graph for Dijkstra and TSP benchmarks."""
    rng = random.Random(seed + num_nodes)
    nodes = [f"N_{i}" for i in range(num_nodes)]
    graph: Dict[str, Dict[str, float]] = {node: {} for node in nodes}

    # Ensure connected backbone (ring)
    for i in range(num_nodes):
        u = nodes[i]
        v = nodes[(i + 1) % num_nodes]
        w = round(rng.uniform(1.0, 15.0), 2)
        graph[u][v] = w
        graph[v][u] = w

    # Add random cross edges
    for i in range(num_nodes):
        for j in range(i + 2, num_nodes):
            if (i == 0 and j == num_nodes - 1):
                continue
            if rng.random() < edge_probability:
                u, v = nodes[i], nodes[j]
                w = round(rng.uniform(1.0, 20.0), 2)
                graph[u][v] = w
                graph[v][u] = w

    return graph


def benchmark_merge_sort(sizes: List[int], repetitions: int = 5) -> Dict[str, Any]:
    """Benchmark Merge Sort across different dataset sizes."""
    timings = []
    for size in sizes:
        parcels = generate_random_parcels(size)
        runs = []
        for _ in range(repetitions):
            data_copy = list(parcels)
            start = time.perf_counter()
            merge_sort(data_copy, key=lambda p: (p["priority"], p["deadline"]))
            elapsed = time.perf_counter() - start
            runs.append(elapsed)
        avg_time = sum(runs) / len(runs)
        timings.append({"size": size, "time_sec": avg_time, "runs": runs})
    return {"algorithm": "Merge Sort", "complexity": "O(n log n)", "data": timings}


def benchmark_knapsack(sizes: List[int], capacity: int = 100, repetitions: int = 3) -> Dict[str, Any]:
    """Benchmark 0/1 Knapsack DP across different item counts."""
    timings = []
    for size in sizes:
        parcels = generate_random_parcels(size)
        runs = []
        for _ in range(repetitions):
            start = time.perf_counter()
            knapsack_01(parcels, capacity=capacity, weight_key="weight", value_key="value")
            elapsed = time.perf_counter() - start
            runs.append(elapsed)
        avg_time = sum(runs) / len(runs)
        timings.append({"size": size, "capacity": capacity, "time_sec": avg_time, "runs": runs})
    return {"algorithm": "0/1 Knapsack DP", "complexity": "O(n * W)", "data": timings}


def benchmark_dijkstra(sizes: List[int], repetitions: int = 5) -> Dict[str, Any]:
    """Benchmark Dijkstra's algorithm across different graph vertex counts."""
    timings = []
    for size in sizes:
        graph = generate_random_connected_graph(size)
        source = "N_0"
        runs = []
        for _ in range(repetitions):
            start = time.perf_counter()
            shortest_paths(graph, source)
            elapsed = time.perf_counter() - start
            runs.append(elapsed)
        avg_time = sum(runs) / len(runs)
        timings.append({"size": size, "time_sec": avg_time, "runs": runs})
    return {"algorithm": "Dijkstra", "complexity": "O((V + E) log V)", "data": timings}


def benchmark_tsp(location_counts: List[int], repetitions: int = 3) -> Dict[str, Any]:
    """Benchmark Nearest Neighbor TSP approximation across numbers of delivery locations."""
    timings = []
    base_graph = generate_random_connected_graph(50)
    depot = "N_0"
    for count in location_counts:
        destinations = [f"N_{i}" for i in range(1, count + 1)]
        runs = []
        for _ in range(repetitions):
            start = time.perf_counter()
            nearest_neighbor_tsp(base_graph, depot=depot, destinations=destinations)
            elapsed = time.perf_counter() - start
            runs.append(elapsed)
        avg_time = sum(runs) / len(runs)
        timings.append({"size": count, "time_sec": avg_time, "runs": runs})
    return {"algorithm": "Nearest Neighbor TSP", "complexity": "O(V^2)", "data": timings}


def run_benchmarks(repetitions: int = 3) -> Dict[str, Any]:
    """Run full benchmarking suite and print summary table."""
    print("Executing Merge Sort Benchmarks...")
    sort_results = benchmark_merge_sort([10, 100, 500, 1000, 2000, 5000], repetitions=repetitions)

    print("Executing 0/1 Knapsack Benchmarks...")
    knap_results = benchmark_knapsack([10, 50, 100, 200, 400], capacity=100, repetitions=repetitions)

    print("Executing Dijkstra Shortest Path Benchmarks...")
    dijk_results = benchmark_dijkstra([10, 25, 50, 100, 200], repetitions=repetitions)

    print("Executing Nearest Neighbor TSP Benchmarks...")
    tsp_results = benchmark_tsp([5, 10, 15, 20, 25], repetitions=repetitions)

    all_results = {
        "sorting": sort_results,
        "knapsack": knap_results,
        "dijkstra": dijk_results,
        "tsp": tsp_results,
    }

    _print_results_summary(all_results)
    return all_results


def _print_results_summary(results: Dict[str, Any]):
    print("\n" + "=" * 65)
    print("              ALGORITHM BENCHMARK TIMING SUMMARY")
    print("=" * 65)
    for key, alg_res in results.items():
        print(f"\n{alg_res['algorithm']} (Theoretical: {alg_res['complexity']}):")
        print(f"  {'Input Size':<15} {'Mean Time (sec)':<20} {'Mean Time (ms)':<15}")
        print("  " + "-" * 50)
        for point in alg_res["data"]:
            sec = point["time_sec"]
            ms = sec * 1000.0
            print(f"  {point['size']:<15} {sec:<20.6f} {ms:<15.3f}")
    print("=" * 65)


if __name__ == "__main__":
    run_benchmarks()
