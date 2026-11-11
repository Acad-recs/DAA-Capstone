# System Design: Mini-Courier Planner

**Course:** Design & Analysis of Algorithms (ETCCDA302)  
**Architecture:** Modular Layered Terminal Application  

---

## 1. Architectural Overview

The application follows clean architectural separation between algorithmic primitives, domain services, data management, and the interactive user presentation layer.

```text
┌─────────────────────────────────────────────────────────────┐
│                    main.py (Presentation)                   │
│        Interactive Terminal UI / CLI Menus & Workflows      │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                  core/ (Application Services)               │
│  - ParcelManager: Validation, storage & sorting integration  │
│  - GraphManager:  Graph validation, lookup & routing proxy  │
│  - CourierPlanner: Multi-stage algorithm pipeline coordinator│
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 algorithms/ (First-Principles Engine)       │
│  - sorting.py:   Stable Merge Sort O(n log n)               │
│  - knapsack.py:  0/1 Knapsack DP O(nW) with Table & Backtrack│
│  - dijkstra.py:  Dijkstra Shortest Paths O((V + E) log V)   │
│  - tsp.py:       Nearest Neighbor TSP Tour O(V^2)           │
└─────────────────────────────────────────────────────────────┘
                               ▲
                               │
┌──────────────────────────────┴──────────────────────────────┐
│                    data/ (JSON Datastores)                  │
│  - parcels.json:   Parcel records with weight, value, etc.  │
│  - locations.json: Campus/city weighted road adjacency list  │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Component Responsibilities

### 2.1 Algorithm Engine (`algorithms/`)
- **`sorting.py` (`merge_sort`, `sort_parcels`):**
  - Implements recursive divide-and-conquer stable Merge Sort.
  - Applies a three-tier comparison tuple `(priority, deadline, parcel_id)` to prioritize parcels deterministically.
- **`knapsack.py` (`knapsack_01`):**
  - Constructs a $(n+1) \times (W+1)$ 2D Dynamic Programming table.
  - Executes backward table trace to isolate exact selected and rejected items without floating-point inaccuracies.
- **`dijkstra.py` (`shortest_paths`, `reconstruct_path`, `all_pairs_shortest_paths`):**
  - Manages priority queue via `heapq`.
  - Disallows negative edge weights and tracks predecessor maps for path reconstruction.
- **`tsp.py` (`nearest_neighbor_tsp`):**
  - Implements greedy nearest-neighbor cycle construction.
  - Returns both the high-level delivery stop order and the expanded road network navigation path.

### 2.2 Core Service Layer (`core/`)
- **`ParcelManager` (`core/parcel_manager.py`):**
  - Enforces schema validation: unique IDs, positive weights, non-negative values, valid deadlines.
- **`GraphManager` (`core/graph_manager.py`):**
  - Validates adjacency list integrity, non-negative edges, and missing neighbor references.
- **`CourierPlanner` (`core/courier_planner.py`):**
  - Orchestrates the multi-stage pipeline and outputs a structured `PlanningResult` dataclass.

### 2.3 Presentation & Execution Layer (`main.py`)
- Provides an intuitive menu-driven CLI.
- Offers independent execution of each algorithm stage as well as the integrated end-to-end planning workflow.

---

## 3. Data Flow Diagram

```text
  [data/parcels.json]             [data/locations.json]
           │                                │
           ▼                                ▼
     ParcelManager                    GraphManager
   (Validate Schema)               (Validate Adjacency)
           │                                │
           ▼                                │
      Merge Sort                            │
   (Order Parcels)                          │
           │                                │
           ▼                                │
     0/1 Knapsack DP                        │
   (Optimal Selection)                      │
           │                                │
           ▼                                │
  Selected Parcels                          │
  & Unique Destinations                     │
           │                                │
           └───────────────┬────────────────┘
                           ▼
                     CourierPlanner
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
        Dijkstra Min-Heap        Nearest Neighbor TSP
     (Pairwise Road Metrics)     (Tour Sequencing)
             │                           │
             └─────────────┬─────────────┘
                           ▼
                    PlanningResult
            (Summary, Route, Distances, Stops)
```
