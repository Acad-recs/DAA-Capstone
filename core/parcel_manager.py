"""Parcel loading and prioritisation services."""

import json
from pathlib import Path

from algorithms.sorting import merge_sort


class ParcelManager:
    """Load parcels and provide priority-ordered views."""

    def __init__(self, data_path):
        self.data_path = Path(data_path)
        self.parcels = self._load()

    def _load(self):
        with self.data_path.open(encoding="utf-8") as file:
            return json.load(file)

    def prioritized(self):
        return merge_sort(self.parcels, key=lambda parcel: -parcel["priority"])
