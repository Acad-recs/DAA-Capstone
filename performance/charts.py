"""Generation of runtime comparison charts using Matplotlib.

Produces 4 standalone publication-ready charts saved in 'outputs/':
1. sorting_runtime.png: Merge Sort Runtime vs Number of Parcels (n)
2. knapsack_runtime.png: 0/1 Knapsack Runtime vs Number of Items (nW)
3. dijkstra_runtime.png: Dijkstra Runtime vs Graph Vertices (V)
4. tsp_runtime.png: Nearest Neighbor TSP Runtime vs Number of Locations (k)
"""

from pathlib import Path
from typing import Any, Dict, List

import matplotlib
matplotlib.use("Agg")  # Non-interactive headless backend
import matplotlib.pyplot as plt

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"


def plot_sorting(sort_data: Dict[str, Any], output_path: Path):
    sizes = [p["size"] for p in sort_data["data"]]
    times_ms = [p["time_sec"] * 1000.0 for p in sort_data["data"]]

    plt.figure(figsize=(8, 5))
    plt.plot(sizes, times_ms, marker="o", color="#2b5c8f", linewidth=2, markersize=6, label="Merge Sort Measured")
    plt.title("Merge Sort: Execution Time vs Input Size (n)", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Number of Parcels (n)", fontsize=11)
    plt.ylabel("Execution Time (milliseconds)", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(fontsize=10)
    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_knapsack(knap_data: Dict[str, Any], output_path: Path):
    sizes = [p["size"] for p in knap_data["data"]]
    times_ms = [p["time_sec"] * 1000.0 for p in knap_data["data"]]

    plt.figure(figsize=(8, 5))
    plt.plot(sizes, times_ms, marker="s", color="#d95f02", linewidth=2, markersize=6, label="0/1 Knapsack DP (W=100)")
    plt.title("0/1 Knapsack DP: Execution Time vs Number of Items (n)", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Number of Items (n) [Capacity W=100]", fontsize=11)
    plt.ylabel("Execution Time (milliseconds)", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(fontsize=10)
    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_dijkstra(dijk_data: Dict[str, Any], output_path: Path):
    sizes = [p["size"] for p in dijk_data["data"]]
    times_ms = [p["time_sec"] * 1000.0 for p in dijk_data["data"]]

    plt.figure(figsize=(8, 5))
    plt.plot(sizes, times_ms, marker="^", color="#1b9e77", linewidth=2, markersize=6, label="Dijkstra (Min-Heap)")
    plt.title("Dijkstra: Execution Time vs Number of Vertices (V)", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Number of Graph Vertices (V)", fontsize=11)
    plt.ylabel("Execution Time (milliseconds)", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(fontsize=10)
    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_tsp(tsp_data: Dict[str, Any], output_path: Path):
    sizes = [p["size"] for p in tsp_data["data"]]
    times_ms = [p["time_sec"] * 1000.0 for p in tsp_data["data"]]

    plt.figure(figsize=(8, 5))
    plt.plot(sizes, times_ms, marker="d", color="#7570b3", linewidth=2, markersize=6, label="Nearest Neighbor TSP")
    plt.title("Nearest Neighbor TSP: Execution Time vs Delivery Locations", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Number of Delivery Locations (k)", fontsize=11)
    plt.ylabel("Execution Time (milliseconds)", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(fontsize=10)
    plt.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()


def generate_all_charts(benchmark_results: Dict[str, Any]) -> List[str]:
    """Generate all 4 runtime comparison charts and return list of saved file paths."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    generated = []

    p1 = OUTPUT_DIR / "sorting_runtime.png"
    plot_sorting(benchmark_results["sorting"], p1)
    generated.append(str(p1))

    p2 = OUTPUT_DIR / "knapsack_runtime.png"
    plot_knapsack(benchmark_results["knapsack"], p2)
    generated.append(str(p2))

    p3 = OUTPUT_DIR / "dijkstra_runtime.png"
    plot_dijkstra(benchmark_results["dijkstra"], p3)
    generated.append(str(p3))

    p4 = OUTPUT_DIR / "tsp_runtime.png"
    plot_tsp(benchmark_results["tsp"], p4)
    generated.append(str(p4))

    return generated
