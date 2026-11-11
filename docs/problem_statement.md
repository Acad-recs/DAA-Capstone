# Problem Statement: Mini-Courier Planner

**Course:** Design & Analysis of Algorithms (ETCCDA302)  
**Project:** Mini-Courier Planner (Capstone Assignment)  
**Language:** Python 3  

---

## 1. Executive Summary & Problem Definition

In modern urban logistics and parcel distribution, delivery services face constrained transport capacity, time-sensitive delivery commitments, and complex road networks. Delivery couriers must optimize:
1. **Parcel Prioritization:** Order incoming packages by urgency rank and delivery deadlines.
2. **Capacity Optimization:** Maximize the total benefit (value) of delivered parcels subject to a strict vehicle payload weight limit ($W$).
3. **Route Planning:** Determine the shortest and most efficient delivery tour that begins at a central depot, visits all selected parcel destinations exactly once, and safely returns to the depot.

The **Mini-Courier Planner** solves this multi-stage algorithmic problem by combining classic computer science algorithms into one deterministic, verified application.

---

## 2. Key Objectives

1. **Prioritize Parcels:** Implement a manual stable **Merge Sort** to order parcels based on priority ranking, deadline urgency, and deterministic tie-breaking.
2. **Optimize Parcel Selection:** Implement **0/1 Knapsack Dynamic Programming** with complete DP table construction and backtracking to find the globally optimal set of parcels that fits vehicle capacity.
3. **Model the Delivery Network:** Represent physical delivery locations as a non-negative weighted graph using an adjacency list.
4. **Calculate Shortest Road Distances:** Implement **Dijkstra's Algorithm** with a binary min-heap (`heapq`) to calculate shortest paths and reconstruct physical routes between road network intersections.
5. **Formulate Delivery Routes:** Implement the **Nearest Neighbor TSP Approximation** heuristic to sequence delivery stops, minimize transit distance, and calculate total tour length including depot return.
6. **Benchmark & Analyze:** Systematically evaluate execution runtimes across variable input sizes ($n$, $W$, $V$, $k$) and provide theoretical and empirical performance comparisons.

---

## 3. Assumptions and Constraints

- **Single Vehicle & Single Depot:** All delivery tours start and end at a designated central hub (`Depot`).
- **Discrete Parcels (0/1 Property):** Parcels cannot be split into fractions; each parcel is either selected entirely or rejected ($x_i \in \{0, 1\}$).
- **Static Road Network:** Road distances between connected locations are fixed, non-negative, and bidirectional.
- **Payload Capacity Constraint:** $\sum_{i \in \text{Selected}} \text{weight}_i \le \text{Capacity}$.
- **Consolidated Stops:** Multiple parcels addressed to the same delivery location are delivered in a single stop.
- **Academic Purity:** All sorting, dynamic programming, shortest path, and routing algorithms are implemented manually from first principles without prebuilt third-party algorithm libraries (such as NetworkX or SciPy).

---

## 4. Input and Output Specifications

### 4.1 Inputs
1. **Parcel Dataset (`data/parcels.json`):**
   - `parcel_id`: Unique string identifier (e.g., `"P001"`).
   - `destination`: Target location string (must correspond to a valid graph node).
   - `weight`: Parcel weight in kg (positive number $> 0$).
   - `value`: Parcel priority value / utility (non-negative number $\ge 0$).
   - `priority`: Priority class integer ($1$ is highest priority).
   - `deadline`: Delivery deadline in relative hours or minutes (positive number $> 0$).

2. **Delivery Location Graph (`data/locations.json`):**
   - Weighted adjacency list mapping each location name to adjacent nodes with edge distances ($\text{km} \ge 0$).

3. **Courier Vehicle Capacity:**
   - Maximum carrying weight limit $W$ (integer kg).

### 4.2 Outputs
1. **Prioritized Parcel Manifest:** Parcels ordered by priority, deadline, and identifier.
2. **0/1 Knapsack Selection Manifest:**
   - Selected parcel list with total loaded weight and total achieved value.
   - Rejected parcel list.
3. **Road Distances:** Shortest physical paths and distances from depot to destinations.
4. **Delivery Tour Plan:**
   - Ordered delivery stop sequence (e.g., `Depot -> Cafeteria -> Hostel -> AdminBlock -> Depot`).
   - Expanded node-by-node turn path.
   - Total route travel distance.
   - Notification of any disconnected/unreachable locations.
