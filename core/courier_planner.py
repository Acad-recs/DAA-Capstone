"""Courier parcel selection and route planning."""

from algorithms.knapsack import knapsack
from algorithms.tsp import nearest_route


class CourierPlanner:
    """Coordinate capacity selection and delivery route planning."""

    def __init__(self, parcels, graph):
        self.parcels = parcels
        self.graph = graph

    def select_parcels(self, capacity):
        return knapsack(self.parcels, capacity)

    def delivery_route(self, start):
        return nearest_route(self.graph, start)
