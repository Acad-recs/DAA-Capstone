# Mini-Courier Planner

**Design & Analysis of Algorithms | ETCCDA302 | Capstone Project**  
**Repository:** `daa-capstone`  
**Language:** Python 3 (Pure Standard Library + Pytest & Matplotlib)  

---

## 1. Project Overview

The **Mini-Courier Planner** is an intelligent dispatch and route optimization application designed to simulate an autonomous parcel delivery system. Given a fleet capacity, a set of time-sensitive parcels, and a complex campus road network, the application:

1. **Prioritizes Parcels:** Orders incoming parcel manifests using a deterministic **Merge Sort** based on priority urgency and delivery deadlines.
2. **Optimizes Payload:** Solves the **0/1 Knapsack Problem** via Dynamic Programming with complete 2D table construction and backtracking to maximize delivered value within vehicle capacity.
3. **Computes Shortest Paths:** Calculates the shortest network paths between all locations using **Dijkstra's Algorithm** with a binary min-heap (`heapq`).
4. **Sequences Delivery Tours:** Solves the Travelling Salesperson Problem (TSP) using the **Nearest Neighbor Approximation Heuristic** to construct an efficient delivery tour that starts and terminates at the depot.
5. **Benchmarks Performance:** Measures execution timings across varying input scales ($n$, $W$, $V$, $k$) and generates comparative runtime graphs.

---

## 2. Architecture & Directory Structure

```text
daa-capstone/
├── algorithms/
│   ├── __init__.py
│   ├── sorting.py          # Stable Merge Sort & parcel prioritization
│   ├── knapsack.py         # 0/1 Knapsack DP (Table + Backtracking)
│   ├── dijkstra.py         # Dijkstra shortest path with Min-Heap
│   └── tsp.py              # Nearest Neighbor TSP tour heuristic
├── core/
│   ├── __init__.py
│   ├── parcel_manager.py   # Dataset loading, validation & schema checks
│   ├── graph_manager.py    # Location graph representation & routing
│   └── courier_planner.py  # End-to-end multi-algorithm pipeline coordinator
├── data/
│   ├── parcels.json        # Parcel dataset (weights, values, priorities, deadlines)
│   └── locations.json      # Weighted adjacency-list campus road network
├── tests/
│   ├── __init__.py
│   ├── test_sorting.py     # Merge sort edge cases, stability & ordering tests
│   ├── test_knapsack.py    # Knapsack DP correctness, capacity & trade-off tests
│   ├── test_dijkstra.py    # Dijkstra shortest path & edge rejection tests
│   ├── test_tsp.py         # TSP route, duplicate stop & disconnect tests
│   └── test_integration.py # Full workflow integration & end-to-end tests
├── performance/
│   ├── benchmark.py        # Microsecond timing across input sizes
│   └── charts.py           # Matplotlib publication chart generator
├── docs/
│   ├── problem_statement.md   # Capstone problem definition & requirements
│   ├── system_design.md       # Architectural patterns & data flow diagrams
│   ├── algorithm_analysis.md  # Formal recurrence, proof sketches & complexities
│   └── viva_preparation.md    # High-frequency viva oral defence Q&A
├── outputs/
│   ├── sorting_runtime.png    # Merge Sort runtime scaling plot
│   ├── knapsack_runtime.png   # 0/1 Knapsack DP runtime scaling plot
│   ├── dijkstra_runtime.png   # Dijkstra runtime scaling plot
│   └── tsp_runtime.png        # Nearest Neighbor TSP scaling plot
├── screenshots/
│   ├── sorting_terminal.png   # Terminal output: Merge Sort
│   ├── knapsack_terminal.png  # Terminal output: 0/1 Knapsack
│   ├── dijkstra_terminal.png  # Terminal output: Dijkstra
│   └── planning_execution.png # Terminal output: Complete End-to-End Tour
├── main.py                 # Interactive terminal CLI application
├── requirements.txt        # Development dependencies (pytest, matplotlib)
├── DEVELOPMENT_LOG.md      # Continuous development progress record
├── LICENSE                 # Project license
└── .gitignore              # Clean repository ignore rules
```

---

## 3. Algorithm Specifications & Complexities

| Algorithm | Module | Time Complexity | Space Complexity | Optimality Status |
|---|---|---|---|---|
| **Merge Sort** | `algorithms/sorting.py` | $\Theta(n \log n)$ | $O(n)$ | Optimal Comparison Sort |
| **0/1 Knapsack DP** | `algorithms/knapsack.py` | $\Theta(nW)$ | $O(nW)$ | Globally Optimal |
| **Dijkstra (Min-Heap)** | `algorithms/dijkstra.py` | $O((V + E) \log V)$ | $O(V + E)$ | Globally Optimal |
| **Nearest Neighbor TSP** | `algorithms/tsp.py` | $O(k^2)$ | $O(k^2)$ | Polynomial Approximation |

*Note: All algorithms are manually implemented from scratch without prebuilt libraries.*

---

## 4. Installation & Setup

### Prerequisites
- Python 3.10+ (Tested on Python 3.12)
- Git

### Setup Virtual Environment
```bash
# Clone the repository
git clone https://github.com/Acad-recs/DAA-Capstone.git
cd DAA-Capstone

# Create and activate virtual environment
python -m venv .venv

# Windows:
.venv\Scripts\activate

# Linux / macOS:
source .venv/bin/activate

# Install testing and charting dependencies
pip install -r requirements.txt
```

---

## 5. Execution Instructions

### 5.1 Interactive Terminal Application
Launch the terminal application:
```bash
python main.py
```

The interactive menu lets you execute each algorithmic phase individually or run the complete automated courier workflow:
```text
====================================================
            MINI-COURIER PLANNER
    Design & Analysis of Algorithms (ETCCDA302)
====================================================

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
```

### 5.2 Automated Testing
Run the complete Pytest suite (36 unit and integration test cases):
```bash
pytest
```

### 5.3 Benchmarking & Visualizations
Run benchmarks and regenerate performance plots in `outputs/`:
```bash
python performance/benchmark.py
```

---

## 6. Sample Application Outputs

### Complete Courier Planning Output
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

## 7. Performance Charts & Screenshots

### Runtime Visualizations (`outputs/`)
- **`outputs/sorting_runtime.png`**: Verifies $O(n \log n)$ scaling from $n=10$ to $n=5,000$ parcels.
- **`outputs/knapsack_runtime.png`**: Demonstrates strict $O(nW)$ linearity across item counts.
- **`outputs/dijkstra_runtime.png`**: Demonstrates $O((V+E)\log V)$ efficiency up to 200 vertices.
- **`outputs/tsp_runtime.png`**: Illustrates smooth $O(k^2)$ scaling for delivery stops.

### Application Screenshots (`screenshots/`)
- **`screenshots/sorting_terminal.png`**: Stable parcel prioritization manifest.
- **`screenshots/knapsack_terminal.png`**: Dynamic programming selection breakdown.
- **`screenshots/dijkstra_terminal.png`**: Predecessor-based shortest road distances.
- **`screenshots/planning_execution.png`**: Full workflow execution trace.

---

## 8. Academic Capstone Verification Summary

| Phase | Assessment Focus | Status | Evidence |
|---|---|---|---|
| **Phase 1** | Courier Problem Design & Planning | **Completed** | Full schema in `data/`, problem statement in `docs/` |
| **Phase 2** | Package Prioritization & Box Filling | **Completed** | Merge Sort (`algorithms/sorting.py`), 0/1 Knapsack DP (`algorithms/knapsack.py`) |
| **Phase 3** | Route Maker & Graph Processing | **Completed** | Dijkstra (`algorithms/dijkstra.py`), Nearest Neighbor TSP (`algorithms/tsp.py`) |
| **Phase 4** | Performance Testing & Optimization | **Completed** | Benchmarking suite (`performance/benchmark.py`), 4 charts in `outputs/` |
| **Phase 5** | Final Report & Demonstration Readiness | **Completed** | Comprehensive README, 36 tests passing, viva guide, interactive CLI |
