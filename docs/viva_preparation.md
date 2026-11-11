# Viva Preparation & Conceptual Q&A: Mini-Courier Planner

**Course:** Design & Analysis of Algorithms (ETCCDA302)  
**Capstone Exam & Oral Defence Reference**

---

## 1. High-Frequency Viva Questions & Model Answers

### Q1: Why was Merge Sort chosen over QuickSort or HeapSort for parcel prioritization?
**Answer:**  
Merge Sort guarantees a strict worst-case time complexity of $O(n \log n)$ regardless of input distribution, avoiding the $O(n^2)$ worst-case degradation that QuickSort suffers on pre-sorted or adversarial inputs. Crucially, Merge Sort is **stable**: it preserves the relative order of parcels with identical priority ranks and deadlines, ensuring fair FIFO dispatch for tied items.

---

### Q2: Why cannot 0/1 Knapsack be solved using a greedy approach like Fractional Knapsack?
**Answer:**  
The greedy choice property fails for 0/1 Knapsack because items cannot be divided. Choosing an item with the highest value-to-weight ratio may leave unfilled capacity that could have accommodated a combination of slightly lower-ratio items yielding a higher total value. Dynamic programming evaluates overlapping subproblems and exhibits optimal substructure, guaranteeing the global optimum.

---

### Q3: What is pseudo-polynomial time, and why does 0/1 Knapsack have it?
**Answer:**  
An algorithm runs in pseudo-polynomial time if its runtime is polynomial in the **numeric value** of an input parameter, but exponential in the **number of bits** required to represent that input. The Knapsack DP runtime is $O(nW)$. The input size of capacity $W$ in binary is $\lceil\log_2 W\rceil = b$ bits. Thus, $W = 2^b$, meaning the complexity is $O(n \cdot 2^b)$, which is exponential with respect to the input length.

---

### Q4: Why does Dijkstra's Algorithm fail when edges have negative weights?
**Answer:**  
Dijkstra's algorithm relies on a greedy property: once a vertex is removed from the priority queue, its shortest distance is considered finalized and never updated again. If a negative edge exists elsewhere in the graph, a longer path could later become shorter through the negative edge, violating Dijkstra's optimality assumption. For negative weights without negative cycles, the Bellman-Ford algorithm ($O(VE)$) must be used instead.

---

### Q5: What is the Travelling Salesperson Problem, and why use Nearest Neighbor instead of brute force?
**Answer:**  
TSP seeks the Hamiltonian cycle of minimum total weight visiting every vertex exactly once and returning to the origin. TSP is NP-hard. Brute force tests $(n-1)!$ permutations, which becomes completely infeasible for even $n = 15$ ($14! \approx 8.7 \times 10^{10}$ operations). Nearest Neighbor provides an $O(k^2)$ polynomial-time greedy approximation suitable for responsive courier dispatch systems.

---

### Q6: How does the system handle disconnected or unreachable destinations?
**Answer:**  
During Dijkstra calculations, unreachable nodes retain a distance of `float('inf')` and have an empty path reconstruction. The `nearest_neighbor_tsp` function explicitly checks reachability from the depot; any unreachable nodes are separated into an `unreachable_destinations` list and reported to the operator, preventing erroneous infinite-distance tours.

---

### Q7: Distinguish between the "Delivery Stop Sequence" and the "Expanded Physical Path".
**Answer:**  
- **Delivery Stop Sequence:** The logical high-level sequence of customer destination vertices where parcels are actually dropped off (e.g., `Depot -> Library -> ScienceBlock -> Depot`).
- **Expanded Physical Path:** The complete turn-by-turn sequence of physical road intersections traversed along the shortest path (e.g., traversing intermediate intersections `Depot -> Cafeteria -> AdminBlock -> Library`).

---

## 2. Algorithm Tracing Walkthrough

### 2.1 Knapsack DP Tracing Example
- Vehicle Capacity $W = 5$
- Parcels:
  - $P_1$: $w = 2, v = 30$
  - $P_2$: $w = 3, v = 40$
  - $P_3$: $w = 4, v = 60$

**DP Table Construction:**
| $i \backslash w$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| **0 (No items)** | 0 | 0 | 0 | 0 | 0 | 0 |
| **1 ($w=2, v=30$)** | 0 | 0 | 30 | 30 | 30 | 30 |
| **2 ($w=3, v=40$)** | 0 | 0 | 30 | 40 | 40 | **70** |
| **3 ($w=4, v=60$)** | 0 | 0 | 30 | 40 | 60 | **70** |

**Backtracking:**
- At $(i=3, w=5)$: $DP[3][5] == DP[2][5] == 70 \implies P_3$ rejected.
- At $(i=2, w=5)$: $DP[2][5] (70) \ne DP[1][5] (30) \implies P_2$ selected! Remaining capacity $= 5 - 3 = 2$.
- At $(i=1, w=2)$: $DP[1][2] (30) \ne DP[0][2] (0) \implies P_1$ selected! Remaining capacity $= 2 - 2 = 0$.
- Selected Items: $\{P_1, P_2\}$, Total Weight $= 5$, Total Value $= 70$.
