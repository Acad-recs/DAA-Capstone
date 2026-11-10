"""Run a small courier planning demonstration."""

from pathlib import Path

from core.courier_planner import CourierPlanner
from core.graph_manager import GraphManager
from core.parcel_manager import ParcelManager


ROOT = Path(__file__).parent


def main():
    parcel_manager = ParcelManager(ROOT / "data" / "parcels.json")
    graph_manager = GraphManager(ROOT / "data" / "locations.json")
    planner = CourierPlanner(parcel_manager.prioritized(), graph_manager.graph)
    selected, value = planner.select_parcels(capacity=10)
    route, distance = planner.delivery_route("Depot")

    print("Selected parcels:", [parcel["id"] for parcel in selected])
    print("Total priority:", value)
    print("Delivery route:", " -> ".join(route))
    print("Route distance:", distance)


if __name__ == "__main__":
    main()
