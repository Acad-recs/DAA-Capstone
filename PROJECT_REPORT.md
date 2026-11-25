# ACADEMIC CAPSTONE PROJECT REPORT

---

# DESIGN & ANALYSIS OF ALGORITHMS (ETCCDA302)
## CAPSTONE PROJECT: MINI-COURIER PLANNER

**Course Code:** ETCCDA302  
**Course Name:** Design & Analysis of Algorithms  
**Project Title:** Mini-Courier Planner  
**Repository:** `daa-capstone`  
**Programming Language:** Python 3  
**Submission Date:** November 2026  

---

## TABLE OF CONTENTS
1. [Executive Summary](#1-executive-summary)
2. [Introduction & Problem Statement](#2-introduction--problem-statement)
3. [System Architecture & Design](#3-system-architecture--design)
4. [Data Design & Network Modeling](#4-data-design--network-modeling)
5. [Algorithm Formulations & Theoretical Analysis](#5-algorithm-formulations--theoretical-analysis)
   - 5.1 [Package Prioritization: Merge Sort](#51-package-prioritization-merge-sort)
   - 5.2 [Payload Optimization: 0/1 Knapsack Dynamic Programming](#52-payload-optimization-01-knapsack-dynamic-programming)
   - 5.3 [Shortest Path Calculation: Dijkstra's Algorithm](#53-shortest-path-calculation-dijkstras-algorithm)
   - 5.4 [Route Sequencing: Nearest Neighbor TSP Approximation](#54-route-sequencing-nearest-neighbor-tsp-approximation)
6. [Integrated Workflow & Execution](#6-integrated-workflow--execution)
7. [Experimental Benchmarking & Empirical Analysis](#7-experimental-benchmarking--empirical-analysis)
8. [Testing & Verification Methodology](#8-testing--verification-methodology)
9. [Conclusion & Future Work](#9-conclusion--future-work)
10. [References](#10-references)

---

## 1. Executive Summary

Urban logistics, express parcel delivery, and automated last-mile dispatch services face complex algorithmic constraints: vehicle payloads are strictly bounded, customer packages carry varying degrees of delivery urgency, and road topologies impose non-trivial routing networks.

The **Mini-Courier Planner** is a computer science capstone application developed for the **Design & Analysis of Algorithms (ETCCDA302)** course. It formulates and implements a unified, deterministic pipeline that coordinates four core algorithmic paradigms:
1. **Divide-and-Conquer (Merge Sort):** Sorts and prioritizes packages by urgency and deadline.
2. **Dynamic Programming (0/1 Knapsack):** Solves the combinatorial optimization problem of selecting the highest-value parcel subset subject to vehicle capacity ($W$).
3. **Greedy Graph Traversal (Dijkstra's Algorithm):** Employs a binary min-heap (`heapq`) to calculate exact shortest road paths.
4. **Heuristic Approximation (Nearest Neighbor TSP):** Formulates an approximate Hamiltonian delivery tour starting and ending at the central depot.

All algorithms are implemented manually from first principles without prebuilt algorithm libraries (such as NetworkX or SciPy), verified through 36 automated unit and integration tests, and benchmarked across scaling input dimensions.

---

## 2. Introduction & Problem Statement

### 2.1 Problem Context
In a courier depot, couriers are presented with an inventory of $n$ packages intended for multiple campus or city delivery locations. The vehicle has a maximum payload weight capacity $W$. Each package $i$ is characterized by:
- A unique parcel ID ($P_i$).
- A delivery destination vertex ($v_i \in V$).
- A weight ($w_i > 0$).
- A delivery priority benefit ($v_i \ge 0$).
- A priority tier ($p_i \in \{1, 2, 3, \dots\}$, where $1$ is highest priority).
- A delivery deadline ($d_i > 0$).

The courier must depart from a designated depot, deliver parcels to their designated destinations without exceeding weight capacity, and return to the depot via the shortest possible overall route.

### 2.2 Formal Problem Objectives
1. **Prioritization:** Order parcels deterministically such that high-priority packages and urgent deadlines receive immediate processing priority.
2. **Knapsack Optimization:** Maximize total delivered utility:
   $$\text{Maximize } \sum_{i=1}^n v_i x_i \quad \text{subject to} \quad \sum_{i=1}^n w_i x_i \le W, \quad x_i \in \{0, 1\}$$
3. **Graph Distance Computation:** For any pair of locations $(u, v) \in V \times V$, determine the shortest path distance $\delta(u, v)$ over a non-negative weighted graph $G = (V, E, \omega)$.
4. **Tour Optimization (TSP):** Find an ordered sequence of delivery stops $[S_0, S_1, S_2, \dots, S_k, S_0]$ where $S_0 = \text{Depot}$, $\{S_1, \dots, S_k\} = \text{UniqueDestinations}$, minimizing total traversal distance:
   $$D = \delta(S_0, S_1) + \sum_{j=1}^{k-1} \delta(S_j, S_{j+1}) + \delta(S_k, S_0)$$

---

## 3. System Architecture & Design

The application adheres to clean separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                 PRESENTATION LAYER (main.py)                │
│         Interactive CLI / Terminal Menu / Visualizations    │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 CORE APPLICATION SERVICES (core/)            │
│  - parcel_manager.py : Schema validation & data access      │
│  - graph_manager.py  : Adjacency list & shortest routing    │
│  - courier_planner.py: Multi-stage pipeline coordinator     │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│              ALGORITHM ENGINE FROM SCRATCH (algorithms/)    │
│  - sorting.py  : Stable Merge Sort (O(n log n))             │
│  - knapsack.py : 0/1 Knapsack DP (O(n * W))                 │
│  - dijkstra.py : Dijkstra with Min-Heap (O((V + E) log V))  │
│  - tsp.py      : Nearest Neighbor TSP Heuristic (O(k^2))    │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Data Design & Network Modeling

### 4.1 Parcel Dataset Schema (`data/parcels.json`)
Each record is validated for schema completeness, positive weight, non-negative value, and uniqueness:
```json
{
  "parcel_id": "P001",
  "destination": "Library",
  "weight": 4,
  "value": 40,
  "priority": 1,
  "deadline": 10
}
```

### 4.2 Delivery Network Graph (`data/locations.json`)
The physical delivery locations are represented as a weighted adjacency list:
- **Vertices ($V=9$):** `Depot`, `Library`, `ScienceBlock`, `Hostel`, `AdminBlock`, `Cafeteria`, `Auditorium`, `SportsComplex`, `EngineeringBlock`.
- **Edges ($E$):** Bidirectional road corridors with physical road lengths in kilometers.

---

## 5. Algorithm Formulations & Theoretical Analysis

### 5.1 Package Prioritization: Merge Sort
- **Paradigm:** Divide-and-Conquer.
- **Recurrence:** $T(n) = 2T(n/2) + \Theta(n) \implies T(n) = \Theta(n \log n)$.
- **Auxiliary Space:** $O(n)$ for auxiliary arrays during merging.
- **Stability:** Maintained by using $\le$ during the merge phase.
- **Ordering Policy Tuple:**
  $$\text{Key}(P) = (\text{priority}, \text{deadline}, \text{parcel\_id})$$
  Ensures strict determinism, favoring priority 1 first, earliest deadline second, and alphabetical tiebreaker third.

### 5.2 Payload Optimization: 0/1 Knapsack Dynamic Programming
- **Paradigm:** Dynamic Programming with complete 2D memoization table and backtracking.
- **Recurrence Relation:**
  Let $DP[i][w]$ denote the maximum value achievable considering a subset of the first $i$ parcels with carrying capacity $w$:
  $$DP[i][w] = \begin{cases}
  0 & \text{if } i = 0 \text{ or } w = 0 \\
  DP[i-1][w] & \text{if } w_i > w \\
  \max\left(DP[i-1][w], \; DP[i-1][w - w_i] + v_i\right) & \text{if } w_i \le w
  \end{cases}$$
- **Time Complexity:** $\Theta(n \cdot W)$ pseudo-polynomial time.
- **Space Complexity:** $\Theta(n \cdot W)$ for the $(n+1) \times (W+1)$ DP table.
- **Item Reconstruction:** Backtracking from $DP[n][W]$ verifies whether $DP[i][w] \ne DP[i-1][w]$. If distinct, item $i$ was included and $w \leftarrow w - w_i$.

### 5.3 Shortest Path Calculation: Dijkstra's Algorithm
- **Paradigm:** Greedy with binary min-heap priority queue (`heapq`).
- **Invariants:** Every vertex popped from the min-heap has its shortest path from the source finalized.
- **Edge Relaxation:**
  $$\text{if } \text{dist}[u] + \text{weight}(u, v) < \text{dist}[v]: \quad \text{dist}[v] \leftarrow \text{dist}[u] + \text{weight}(u, v), \quad \text{prev}[v] \leftarrow u$$
- **Time Complexity:** $O((V + E) \log V)$ with adjacency list and min-heap.
- **Space Complexity:** $O(V + E)$ storing distances, predecessors, and the graph.
- **Integrity:** Enforces strict non-negative edge weight verification.

### 5.4 Route Sequencing: Nearest Neighbor TSP Approximation
- **Paradigm:** Greedy heuristic approximation for NP-hard TSP.
- **Procedure:** Starting at `Depot`, iteratively find $\arg\min_{u \in \text{Unvisited}} \delta(\text{current}, u)$, move to $u$, and finally return to `Depot`.
- **Time Complexity:** $O(k^2)$ over the precomputed pairwise distance matrix.
- **Space Complexity:** $O(k^2)$ for pairwise distance cache.
- **Distinction:** Distinguishes between the customer stop sequence (destination nodes) and the expanded physical path (all road intersections traversed).

---

## 6. Integrated Workflow & Execution

The complete courier workflow coordinates all four algorithms:
1. Load parcel manifests and road network.
2. Sort parcels via Merge Sort.
3. Optimize loaded parcel set via 0/1 Knapsack DP.
4. Extract unique destinations from selected parcels.
5. Compute shortest paths using Dijkstra.
6. Generate delivery tour using Nearest Neighbor TSP.
7. Print formatted execution summary.

### Execution Output:
```text
==================================================
       MINI-COURIER PLANNER - EXECUTION SUMMARY
==================================================
Depot Location:           Depot
Vehicle Capacity:         15 kg
Total Available Parcels:  10
Selected Parcels:         4
Rejected Parcels:         6
Total Loaded Weight:      15 / 15 kg
Total Achieved Value:     155
--------------------------------------------------
Delivery Destinations:    Cafeteria, EngineeringBlock, Hostel, Library
Delivery Stop Sequence:   Depot -> Cafeteria -> Library -> EngineeringBlock -> Hostel -> Depot
Expanded Physical Path:   Depot -> Cafeteria -> Auditorium -> Library -> ScienceBlock -> EngineeringBlock -> SportsComplex -> Hostel -> Depot
Total Travel Distance:    22.00 km/units
==================================================
```

---

## 7. Experimental Benchmarking & Empirical Analysis

High-resolution timing benchmarks were executed using Python's `time.perf_counter()` across varying input sizes.

### 7.1 Empirical Timing Results
| Algorithm | Input Parameter | Input Range | Observed Mean Time | Theoretical Complexity |
|---|---|---|---|---|
| **Merge Sort** | Number of parcels ($n$) | $10 \to 5,000$ | $0.038\text{ ms} \to 51.163\text{ ms}$ | $\Theta(n \log n)$ |
| **0/1 Knapsack DP** | Item count ($n, W=100$) | $10 \to 400$ | $0.369\text{ ms} \to 14.085\text{ ms}$ | $\Theta(n W)$ |
| **Dijkstra** | Vertices ($V$) | $10 \to 200$ | $0.062\text{ ms} \to 6.863\text{ ms}$ | $O((V+E)\log V)$ |
| **Nearest Neighbor TSP** | Delivery locations ($k$) | $5 \to 25$ | $3.824\text{ ms} \to 17.251\text{ ms}$ | $O(k^2)$ |

### 7.2 Visual Artifacts Generated
- `outputs/sorting_runtime.png`: Demonstrates classic $n \log n$ curve.
- `outputs/knapsack_runtime.png`: Confirms strict linear dependence on $n$ when capacity $W$ is held constant.
- `outputs/dijkstra_runtime.png`: Exhibits sub-quadratic $O((V+E)\log V)$ performance.
- `outputs/tsp_runtime.png`: Confirms quadratic $O(k^2)$ polynomial growth.

---

## 8. Testing & Verification Methodology

Automated testing was conducted using Pytest on Python 3.12:
- **Total Test Cases:** 36 passed / 0 failed in 0.56s.
- **Coverage Highlights:**
  - `test_sorting.py` (11 tests): Empty input, single element, negative numbers, stability preservation, multi-key ordering.
  - `test_knapsack.py` (8 tests): Zero capacity, oversize items, exact weight matches, DP vs greedy optimality verification.
  - `test_dijkstra.py` (6 tests): Direct paths, multi-hop paths, negative edge weight rejection, disconnected subgraphs.
  - `test_tsp.py` (7 tests): Single location, multiple locations, duplicate destination deduplication, disconnected nodes.
  - `test_integration.py` (4 tests): Full pipeline coordination, insufficient capacity, high capacity limits.

---

## 9. Conclusion & Future Work

The **Mini-Courier Planner** successfully achieves all academic objectives of the ETCCDA302 capstone assignment. By enforcing first-principles implementations, mathematical correctness, strict schema validation, comprehensive unit testing, and empirical benchmarking, the project bridges algorithmic theory with real-world logistics applications.

### Future Enhancements:
1. **Dynamic Time Windows (VRPTW):** Incorporating hard delivery time windows into the TSP heuristic.
2. **Multi-Vehicle Fleets (mTSP):** Extending Knapsack and TSP to support multiple couriers departing from one depot.
3. **Advanced Meta-heuristics:** Implementing 2-Opt or Simulated Annealing to further refine the initial Nearest Neighbor TSP tour.

---

## 10. References
1. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to Algorithms* (4th ed.). MIT Press.
2. Kleinberg, J., & Tardos, É. (2006). *Algorithm Design*. Pearson.
3. Applegate, D. L., Bixby, R. E., Chvátal, V., & Cook, W. J. (2006). *The Traveling Salesman Problem: A Computational Study*. Princeton University Press.
