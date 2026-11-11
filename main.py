#!/usr/bin/env python3
"""Mini-Courier Planner - Interactive Terminal Application.

Course: Design & Analysis of Algorithms (ETCCDA302)
Capstone Assignment - Terminal Interface
"""

import sys
from pathlib import Path
from typing import Optional

from core.courier_planner import CourierPlanner
from core.graph_manager import GraphManager
from core.parcel_manager import ParcelManager
from performance.benchmark import run_benchmarks
from performance.charts import generate_all_charts

ROOT = Path(__file__).resolve().parent
DEFAULT_PARCELS_FILE = ROOT / "data" / "parcels.json"
DEFAULT_LOCATIONS_FILE = ROOT / "data" / "locations.json"
DEFAULT_CAPACITY = 15
DEFAULT_DEPOT = "Depot"


def clear_banner():
    print("\n" + "=" * 52)
    print("            MINI-COURIER PLANNER")
    print("    Design & Analysis of Algorithms (ETCCDA302)")
    print("=" * 52)


def display_menu():
    print("""
[1] View Parcel Dataset
[2] Sort and Prioritize Parcels (Merge Sort)
[3] Optimize Parcel Selection (0/1 Knapsack DP)
[4] View Delivery Location Graph
[5] Calculate Shortest Paths (Dijkstra's Algorithm)
[6] Generate Delivery Route (Nearest Neighbor TSP)
[7] Run Complete Courier Planning Workflow
[8] Run Performance Benchmarks & Generate Charts
[9] View Project & Algorithm Information
[0] Exit
""")
    print("=" * 52)


def view_parcels(parcel_mgr: ParcelManager):
    print("\n--- AVAILABLE PARCELS ---")
    print(f"{'ID':<6} {'Destination':<18} {'Weight (kg)':<12} {'Value':<8} {'Priority':<10} {'Deadline':<8}")
    print("-" * 66)
    for p in parcel_mgr.parcels:
        print(f"{p['parcel_id']:<6} {p['destination']:<18} {p['weight']:<12} {p['value']:<8} {p['priority']:<10} {p['deadline']:<8}")
    print("-" * 66)
    print(f"Total Parcels: {len(parcel_mgr.parcels)} | Total Weight: {parcel_mgr.total_weight()} kg | Total Value: {parcel_mgr.total_value()}")


def sort_and_prioritize(parcel_mgr: ParcelManager):
    print("\n--- SORTED & PRIORITIZED PARCELS (MERGE SORT) ---")
    print("Ordering Policy: Priority Ascending (1 is highest), Deadline Earliest First, Parcel ID Tiebreaker")
    print(f"{'Rank':<6} {'ID':<6} {'Priority':<10} {'Deadline':<10} {'Destination':<18} {'Weight':<8} {'Value':<6}")
    print("-" * 68)
    sorted_parcels = parcel_mgr.prioritized()
    for rank, p in enumerate(sorted_parcels, 1):
        print(f"{rank:<6} {p['parcel_id']:<6} {p['priority']:<10} {p['deadline']:<10} {p['destination']:<18} {p['weight']:<8} {p['value']:<6}")
    print("-" * 68)
    print("Algorithm: Merge Sort | Time: O(n log n) | Space: O(n) | Stable: Yes")


def optimize_knapsack(planner: CourierPlanner):
    print("\n--- OPTIMIZE PARCEL SELECTION (0/1 KNAPSACK DP) ---")
    cap_input = input(f"Enter vehicle carrying capacity (default {DEFAULT_CAPACITY} kg): ").strip()
    capacity = int(cap_input) if cap_input.isdigit() else DEFAULT_CAPACITY

    selected, rejected, total_w, total_v, _ = planner.select_parcels(capacity)
    print(f"\nOptimization Result for Vehicle Capacity = {capacity} kg:")
    print("-" * 60)
    print(f"Selected Parcels ({len(selected)}):")
    for p in selected:
        print(f"  [+] {p['parcel_id']}: Dest={p['destination']}, Weight={p['weight']} kg, Value={p['value']}, Priority={p['priority']}")
    print(f"\nRejected Parcels ({len(rejected)}):")
    for p in rejected:
        print(f"  [-] {p['parcel_id']}: Dest={p['destination']}, Weight={p['weight']} kg, Value={p['value']}")
    print("-" * 60)
    print(f"Total Loaded Weight: {total_w} / {capacity} kg (Utilization: {(total_w / capacity) * 100:.1f}%)")
    print(f"Total Achieved Value: {total_v}")
    print("Algorithm: 0/1 Knapsack DP | Time: O(n * W) | Space: O(n * W)")


def view_graph(graph_mgr: GraphManager):
    print("\n--- DELIVERY LOCATION ROAD NETWORK (ADJACENCY LIST) ---")
    for node, neighbors in graph_mgr.graph.items():
        edges_str = ", ".join(f"{nbr}: {dist} km" for nbr, dist in neighbors.items())
        print(f"  {node:<18} -> {edges_str}")
    print(f"\nTotal Locations (Vertices): {len(graph_mgr.graph)}")


def calculate_shortest_paths(graph_mgr: GraphManager):
    print("\n--- SHORTEST PATHS (DIJKSTRA'S ALGORITHM) ---")
    source = input(f"Enter source vertex (default '{DEFAULT_DEPOT}'): ").strip() or DEFAULT_DEPOT
    if source not in graph_mgr.graph:
        print(f"Error: '{source}' does not exist in delivery graph.")
        return

    destinations = [n for n in graph_mgr.graph if n != source]
    print(f"\nShortest paths from origin '{source}':")
    print(f"{'Target Location':<20} {'Distance (km)':<15} {'Shortest Physical Path':<30}")
    print("-" * 68)
    for target in destinations:
        path, distance = graph_mgr.route(source, target)
        dist_str = f"{distance:.2f}" if distance < float("inf") else "UNREACHABLE"
        path_str = " -> ".join(path) if path else "None"
        print(f"{target:<20} {dist_str:<15} {path_str:<30}")
    print("-" * 68)
    print("Algorithm: Dijkstra with Min-Heap | Time: O((V + E) log V) | Space: O(V + E)")


def generate_delivery_route(planner: CourierPlanner):
    print("\n--- GENERATE DELIVERY ROUTE (NEAREST NEIGHBOR TSP) ---")
    dest_input = input("Enter comma-separated destination names (leave empty to use all graph nodes): ").strip()
    if dest_input:
        destinations = [d.strip() for d in dest_input.split(",") if d.strip()]
    else:
        destinations = [n for n in planner.graph if n != DEFAULT_DEPOT]

    stops, exp_path, dist, unreachable = planner.plan_route_for_destinations(destinations, depot=DEFAULT_DEPOT)
    print("\nDelivery Tour Route:")
    print(f"  Stop Sequence: {' -> '.join(stops)}")
    print(f"  Expanded Path: {' -> '.join(exp_path)}")
    print(f"  Total Distance: {dist:.2f} km")
    if unreachable:
        print(f"  Unreachable Locations: {', '.join(unreachable)}")
    print("Algorithm: Nearest Neighbor TSP Approximation | Time: O(V^2) | Space: O(V^2)")


def run_complete_workflow(planner: CourierPlanner):
    print("\n--- RUN COMPLETE INTEGRATED COURIER PLANNING WORKFLOW ---")
    cap_input = input(f"Enter vehicle capacity (default {DEFAULT_CAPACITY} kg): ").strip()
    capacity = int(cap_input) if cap_input.isdigit() else DEFAULT_CAPACITY

    result = planner.plan(capacity=capacity, depot=DEFAULT_DEPOT)
    print("\n" + result.summary())


def run_benchmarks_and_charts():
    print("\n--- RUNNING PERFORMANCE BENCHMARKS ---")
    results = run_benchmarks(repetitions=5)
    print("\nGenerating comparative charts in 'outputs/'...")
    chart_paths = generate_all_charts(results)
    print("Generated Chart Files:")
    for path in chart_paths:
        print(f"  - {path}")
    print("\nBenchmark and chart generation complete.")


def view_project_info():
    print("""
============================================================
              PROJECT & ALGORITHM INFORMATION
============================================================
Course:       Design & Analysis of Algorithms (ETCCDA302)
Project:      Mini-Courier Planner (Capstone)
Repository:   daa-capstone
Language:     Python 3 (Standard Library + Pytest & Matplotlib)

Algorithms Implemented:
1. Merge Sort:
   - File: algorithms/sorting.py
   - Usage: Prioritizing parcels by delivery urgency and deadline.
   - Complexity: Time O(n log n), Auxiliary Space O(n).

2. 0/1 Knapsack (Dynamic Programming):
   - File: algorithms/knapsack.py
   - Usage: Selecting optimal parcel set within vehicle capacity.
   - Recurrence: DP[i][w] = max(DP[i-1][w], DP[i-1][w-wt[i-1]] + val[i-1])
   - Complexity: Time O(n * W), Space O(n * W).

3. Dijkstra's Shortest Path:
   - File: algorithms/dijkstra.py
   - Usage: Finding shortest road paths between depot and stops.
   - Complexity: Time O((V + E) log V), Space O(V + E).

4. Nearest Neighbor TSP Approximation:
   - File: algorithms/tsp.py
   - Usage: Approximating the shortest delivery tour starting and ending at depot.
   - Complexity: Time O(V^2), Space O(V^2).
============================================================
""")


def main():
    try:
        parcel_mgr = ParcelManager(DEFAULT_PARCELS_FILE)
        graph_mgr = GraphManager(DEFAULT_LOCATIONS_FILE)
        planner = CourierPlanner(parcel_mgr.parcels, graph_mgr.graph, depot=DEFAULT_DEPOT)
    except Exception as exc:
        print(f"Error loading initial dataset files: {exc}", file=sys.stderr)
        sys.exit(1)

    while True:
        clear_banner()
        display_menu()
        choice = input("Enter your choice (0-9): ").strip()

        if choice == "1":
            view_parcels(parcel_mgr)
        elif choice == "2":
            sort_and_prioritize(parcel_mgr)
        elif choice == "3":
            optimize_knapsack(planner)
        elif choice == "4":
            view_graph(graph_mgr)
        elif choice == "5":
            calculate_shortest_paths(graph_mgr)
        elif choice == "6":
            generate_delivery_route(planner)
        elif choice == "7":
            run_complete_workflow(planner)
        elif choice == "8":
            run_benchmarks_and_charts()
        elif choice == "9":
            view_project_info()
        elif choice == "0":
            print("\nThank you for using Mini-Courier Planner. Goodbye!")
            sys.exit(0)
        else:
            print(f"\nInvalid choice '{choice}'. Please select a valid option from 0 to 9.")

        input("\nPress [Enter] to return to the main menu...")


if __name__ == "__main__":
    main()
