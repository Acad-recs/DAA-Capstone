"""Courier parcel selection, prioritization, and delivery route planning integration."""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Tuple

from algorithms.dijkstra import all_pairs_shortest_paths, shortest_paths
from algorithms.knapsack import knapsack_01
from algorithms.sorting import sort_parcels
from algorithms.tsp import nearest_neighbor_tsp


@dataclass
class PlanningResult:
    """Encapsulates the end-to-end output of the courier planning workflow."""

    all_parcels: List[Dict[str, Any]]
    prioritized_parcels: List[Dict[str, Any]]
    selected_parcels: List[Dict[str, Any]]
    rejected_parcels: List[Dict[str, Any]]
    vehicle_capacity: int
    total_selected_weight: int
    total_selected_value: int
    delivery_destinations: List[str]
    unique_destinations: List[str]
    depot: str
    stop_sequence: List[str]
    expanded_path: List[str]
    total_route_distance: float
    unreachable_destinations: List[str]
    dp_table: Optional[List[List[int]]] = None

    def summary(self) -> str:
        """Format a clear human-readable summary of planning results."""
        lines = [
            "=" * 50,
            "       MINI-COURIER PLANNER - EXECUTION SUMMARY",
            "=" * 50,
            f"Depot Location:           {self.depot}",
            f"Vehicle Capacity:         {self.vehicle_capacity} kg",
            f"Total Available Parcels:  {len(self.all_parcels)}",
            f"Selected Parcels:         {len(self.selected_parcels)}",
            f"Rejected Parcels:         {len(self.rejected_parcels)}",
            f"Total Loaded Weight:      {self.total_selected_weight} / {self.vehicle_capacity} kg",
            f"Total Achieved Value:     {self.total_selected_value}",
            "-" * 50,
            f"Delivery Destinations:    {', '.join(self.unique_destinations) if self.unique_destinations else 'None'}",
            f"Delivery Stop Sequence:   {' -> '.join(self.stop_sequence)}",
            f"Expanded Physical Path:   {' -> '.join(self.expanded_path)}",
            f"Total Travel Distance:    {self.total_route_distance:.2f} km/units",
        ]
        if self.unreachable_destinations:
            lines.append(f"UNREACHABLE DESTINATIONS: {', '.join(self.unreachable_destinations)}")
        lines.append("=" * 50)
        return "\n".join(lines)


class CourierPlanner:
    """Coordinates parcel prioritization, knapsack optimization, and route planning."""

    def __init__(self, parcels: List[Dict[str, Any]], graph: Dict[str, Dict[str, float]], depot: str = "Depot"):
        self.parcels = parcels
        self.graph = graph
        self.depot = depot

    def prioritize_parcels(self) -> List[Dict[str, Any]]:
        """Sort parcels according to priority rank and delivery deadline."""
        return sort_parcels(self.parcels)

    def select_parcels(
        self,
        capacity: int,
        parcels: Optional[List[Dict[str, Any]]] = None,
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], int, int, List[List[int]]]:
        """Apply 0/1 Knapsack dynamic programming to select the optimal subset of parcels."""
        candidate_parcels = parcels if parcels is not None else self.prioritize_parcels()
        return knapsack_01(candidate_parcels, capacity=capacity, weight_key="weight", value_key="value")

    def plan_route_for_destinations(
        self,
        destinations: List[str],
        depot: Optional[str] = None,
    ) -> Tuple[List[str], List[str], float, List[str]]:
        """Compute delivery route using Dijkstra and Nearest Neighbor TSP."""
        start_depot = depot or self.depot
        return nearest_neighbor_tsp(self.graph, depot=start_depot, destinations=destinations)

    def plan(self, capacity: int, depot: Optional[str] = None) -> PlanningResult:
        """Execute the complete end-to-end courier planning workflow.

        Workflow:
        1. Prioritize parcels using Merge Sort (priority, deadline).
        2. Apply 0/1 Knapsack optimization to select optimal parcel combination within capacity.
        3. Identify unique delivery destinations from selected parcels.
        4. Calculate shortest paths and generate delivery route using Nearest Neighbor TSP.
        5. Return encapsulated PlanningResult.
        """
        start_depot = depot or self.depot
        prioritized = self.prioritize_parcels()
        selected, rejected, total_w, total_v, dp_table = self.select_parcels(capacity, parcels=prioritized)

        # Extract destinations
        destinations = [p["destination"] for p in selected]
        unique_destinations = sorted(list(set(destinations)))

        # Solve TSP route
        stop_seq, exp_path, route_dist, unreachable = self.plan_route_for_destinations(
            destinations=destinations,
            depot=start_depot,
        )

        return PlanningResult(
            all_parcels=self.parcels,
            prioritized_parcels=prioritized,
            selected_parcels=selected,
            rejected_parcels=rejected,
            vehicle_capacity=capacity,
            total_selected_weight=total_w,
            total_selected_value=total_v,
            delivery_destinations=destinations,
            unique_destinations=unique_destinations,
            depot=start_depot,
            stop_sequence=stop_seq,
            expanded_path=exp_path,
            total_route_distance=route_dist,
            unreachable_destinations=unreachable,
            dp_table=dp_table,
        )

    # Backward-compatible convenience methods
    def delivery_route(self, start: str) -> Tuple[List[str], float]:
        stops, _, dist, _ = self.plan_route_for_destinations(
            destinations=[node for node in self.graph if node != start],
            depot=start,
        )
        return stops, dist
