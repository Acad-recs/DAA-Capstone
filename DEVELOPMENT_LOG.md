# Development Log: Mini-Courier Planner (DAA Capstone)

This log records milestones, commits, testing results, benchmarks, and issue resolutions across the continuous development run.

---

## 1. Initial State Analysis
- **Base Commit**: `c10df98` ("Implement courier planning system with algorithms for parcel selection and route optimization")
- **Initial Working Tree**: Minimal prototypes, missing required parcel attributes (value, deadline), TSP implemented as brute-force permutation search instead of Nearest Neighbor heuristic, missing interactive terminal CLI, missing comprehensive test suites, missing benchmarks and charts, missing detailed academic documentation. Tracked `.pyc` files present in Git.

---

## 2. Development Milestones & Git Commit History

| Commit | Hash | Message | Summary of Completed Scope |
|---:|:---:|---|---|
| **01** | `11051b6` | `chore: initialize project structure and gitignore configuration` | Cleaned tracked `.pyc` files, added comprehensive `.gitignore`, updated `requirements.txt`, initialized development log. |
| **02** | `4ba3b23` | `feat: expand parcel and delivery location datasets with complete schemas` | Expanded `parcels.json` (10 items with `parcel_id`, `destination`, `weight`, `value`, `priority`, `deadline`) and `locations.json` (9 connected campus locations). |
| **03** | `edb42f8` | `feat: implement parcel data validation and management services` | Implemented strict validation in `ParcelManager` (positive weights, non-negative values, unique IDs, positive deadlines). |
| **04** | `791e863` | `feat: implement manual merge sort algorithm with deterministic parcel ordering` | Implemented manual stable Merge Sort in `algorithms/sorting.py` with multi-key parcel ordering policy `(priority, deadline, parcel_id)`. |
| **05** | `5aa4dc1` | `feat: add comprehensive parcel prioritization and merge sort tests` | 11 unit tests in `tests/test_sorting.py` covering empty lists, single elements, reverse order, stability, and deadline tiebreaking. |
| **06** | `6abe80a` | `feat: implement 0/1 knapsack dynamic programming with full DP table and backtracking` | Implemented 0/1 Knapsack DP in `algorithms/knapsack.py` with full $(n+1) \times (W+1)$ DP table construction and backtracking reconstruction. |
| **07** | `5447ea4` | `feat: add comprehensive knapsack test suite for edge cases and optimal parcel selection` | 8 unit tests in `tests/test_knapsack.py` testing zero capacity, oversized items, DP vs greedy optimality, and table dimensions. |
| **08** | `027ddcb` | `feat: implement weighted delivery graph validation and query operations` | Implemented `GraphManager` in `core/graph_manager.py` with adjacency list validation, non-negative weight checks, and route queries. |
| **09** | `8e0f6ed` | `feat: implement dijkstra shortest path algorithm with path reconstruction and pairwise matrix` | Implemented Dijkstra's algorithm with binary min-heap (`heapq`), path reconstruction, disconnected handling, and all-pairs matrix. |
| **10** | `d737ba4` | `test: add comprehensive dijkstra edge case and path reconstruction validation` | 6 unit tests in `tests/test_dijkstra.py` verifying path reconstruction, disconnected graphs, negative weight rejection, and all-pairs shortest paths. |
| **11** | `3f58a64` | `feat: implement nearest neighbor tsp approximation with expanded physical path` | Implemented `nearest_neighbor_tsp` in `algorithms/tsp.py`, computing stop sequences, expanded physical paths, depot return, and unreachable destination detection. |
| **12** | `37a4175` | `feat: integrate complete courier planning workflow coordinating all algorithms` | Implemented `CourierPlanner.plan()` returning `PlanningResult` combining Merge Sort, Knapsack DP, Dijkstra, and Nearest Neighbor TSP. |
| **13** | `96d92fa` | `test: add integration test suite covering end-to-end planning workflow` | 4 integration tests in `tests/test_integration.py` verifying complete pipeline execution, capacity constraints, and depot tours. |
| **14** | `9632cc8` | `feat: build interactive terminal application with modular menu and workflow execution` | Interactive CLI menu in `main.py` supporting independent algorithm execution and the complete courier workflow. |
| **15** | `9f3ae57` | `feat: implement algorithm benchmarking framework and runtime visualization charts` | Benchmarking framework in `performance/benchmark.py` and Matplotlib charts generator in `performance/charts.py` generating 4 publication plots in `outputs/`. |
| **16** | `PENDING` | `docs: finalize capstone documentation, screenshots, and viva preparation guide` | Complete `README.md`, technical Markdown docs (`docs/`), terminal execution screenshots in `screenshots/`, and final verification report. |

---

## 3. Testing & Validation Summary
- **Test Runner**: `pytest-9.2.0` on Python 3.12.10
- **Total Test Cases**: 36 passed / 0 failed / 0 skipped in 0.31s
- **Breakdown**:
  - `tests/test_sorting.py`: 11 passed
  - `tests/test_knapsack.py`: 8 passed
  - `tests/test_dijkstra.py`: 6 passed
  - `tests/test_tsp.py`: 7 passed
  - `tests/test_integration.py`: 4 passed

---

## 4. Benchmark & Performance Summary

Empirical timings collected via `time.perf_counter()` (averaged over multiple runs):

| Algorithm | Input Parameter | Input Range | Observed Mean Time | Complexity Fit |
|---|---|---|---|---|
| **Merge Sort** | Number of parcels ($n$) | $10 \to 5,000$ | $0.038\text{ ms} \to 51.163\text{ ms}$ | $\Theta(n \log n)$ |
| **0/1 Knapsack DP** | Number of items ($n, W=100$) | $10 \to 400$ | $0.369\text{ ms} \to 14.085\text{ ms}$ | $\Theta(n W)$ |
| **Dijkstra** | Graph vertices ($V$) | $10 \to 200$ | $0.062\text{ ms} \to 6.863\text{ ms}$ | $O((V+E)\log V)$ |
| **Nearest Neighbor TSP** | Delivery locations ($k$) | $5 \to 25$ | $3.824\text{ ms} \to 17.251\text{ ms}$ | $O(k^2)$ |

Generated charts in `outputs/`:
- `sorting_runtime.png`
- `knapsack_runtime.png`
- `dijkstra_runtime.png`
- `tsp_runtime.png`

Generated terminal execution screenshots in `screenshots/`:
- `sorting_terminal.png`
- `knapsack_terminal.png`
- `dijkstra_terminal.png`
- `planning_execution.png`

---

## 5. Capstone Assessment Phase Verification

- **Phase 1: Problem Design & Planning** -> COMPLETE
- **Phase 2: Package Prioritization & Box Filling** -> COMPLETE
- **Phase 3: Route Maker & Graph Processing** -> COMPLETE
- **Phase 4: Performance Testing & Optimization** -> COMPLETE
- **Phase 5: Final Report & Demonstration Readiness** -> COMPLETE
