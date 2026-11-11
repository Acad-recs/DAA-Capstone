"""Integration and end-to-end tests for the complete Mini-Courier Planner workflow."""

import unittest
from pathlib import Path

from core.courier_planner import CourierPlanner
from core.graph_manager import GraphManager
from core.parcel_manager import ParcelManager

ROOT = Path(__file__).resolve().parent.parent


class TestIntegration(unittest.TestCase):
    """Verify data loading, end-to-end algorithm coordination, and planning results."""

    def setUp(self):
        self.parcels_path = ROOT / "data" / "parcels.json"
        self.locations_path = ROOT / "data" / "locations.json"

    def test_datasets_exist_and_load_cleanly(self):
        parcel_mgr = ParcelManager(self.parcels_path)
        graph_mgr = GraphManager(self.locations_path)

        self.assertGreater(len(parcel_mgr.parcels), 0)
        self.assertGreater(len(graph_mgr.graph), 0)
        self.assertIn("Depot", graph_mgr.graph)

    def test_end_to_end_planning_workflow(self):
        parcel_mgr = ParcelManager(self.parcels_path)
        graph_mgr = GraphManager(self.locations_path)
        planner = CourierPlanner(parcel_mgr.parcels, graph_mgr.graph, depot="Depot")

        capacity = 15
        result = planner.plan(capacity=capacity)

        # 1. Knapsack constraint validation
        self.assertLessEqual(result.total_selected_weight, capacity)
        self.assertEqual(
            result.total_selected_weight,
            sum(p["weight"] for p in result.selected_parcels),
        )
        self.assertEqual(
            result.total_selected_value,
            sum(p["value"] for p in result.selected_parcels),
        )
        self.assertEqual(
            len(result.selected_parcels) + len(result.rejected_parcels),
            len(result.all_parcels),
        )

        # 2. Destinations and TSP tour validation
        selected_destinations = {p["destination"] for p in result.selected_parcels}
        self.assertEqual(set(result.unique_destinations), selected_destinations)

        if result.unique_destinations:
            # Tour starts and ends at Depot
            self.assertEqual(result.stop_sequence[0], "Depot")
            self.assertEqual(result.stop_sequence[-1], "Depot")
            # Every selected destination is in stop sequence
            for dest in result.unique_destinations:
                self.assertIn(dest, result.stop_sequence)
            self.assertGreater(result.total_route_distance, 0.0)

    def test_planning_with_insufficient_capacity(self):
        parcel_mgr = ParcelManager(self.parcels_path)
        graph_mgr = GraphManager(self.locations_path)
        planner = CourierPlanner(parcel_mgr.parcels, graph_mgr.graph, depot="Depot")

        # Capacity 1 is less than smallest parcel weight (which is 2)
        result = planner.plan(capacity=1)
        self.assertEqual(len(result.selected_parcels), 0)
        self.assertEqual(result.total_selected_weight, 0)
        self.assertEqual(result.total_selected_value, 0)
        self.assertEqual(result.stop_sequence, ["Depot"])
        self.assertEqual(result.total_route_distance, 0.0)

    def test_planning_with_large_capacity(self):
        parcel_mgr = ParcelManager(self.parcels_path)
        graph_mgr = GraphManager(self.locations_path)
        planner = CourierPlanner(parcel_mgr.parcels, graph_mgr.graph, depot="Depot")

        # Capacity larger than total sum of all parcel weights
        huge_capacity = 1000
        result = planner.plan(capacity=huge_capacity)
        self.assertEqual(len(result.selected_parcels), len(result.all_parcels))
        self.assertEqual(len(result.rejected_parcels), 0)


if __name__ == "__main__":
    unittest.main()
