"""Parcel loading, management, and validation services."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from algorithms.sorting import sort_parcels


class ParcelManager:
    """Manages parcel records with strict schema validation and prioritization."""

    REQUIRED_FIELDS = {"parcel_id", "destination", "weight", "value", "priority", "deadline"}

    def __init__(self, data_path: Optional[Path] = None, parcels: Optional[List[Dict[str, Any]]] = None):
        """Initialize ParcelManager from a file path or a raw list of parcel dictionaries."""
        self.data_path = Path(data_path) if data_path else None
        if parcels is not None:
            self.parcels = self.validate_parcels(parcels)
        elif self.data_path is not None:
            self.parcels = self._load()
        else:
            self.parcels = []

    def _load(self) -> List[Dict[str, Any]]:
        """Load parcel data from JSON file with validation."""
        if not self.data_path.exists():
            raise FileNotFoundError(f"Parcel dataset file not found: {self.data_path}")
        with self.data_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            raise ValueError("Parcel dataset must contain a JSON array of parcel objects.")
        return self.validate_parcels(data)

    @classmethod
    def validate_parcels(cls, parcels: List[Dict[str, Any]], valid_locations: Optional[Set[str]] = None) -> List[Dict[str, Any]]:
        """Validate an array of parcel dictionaries.

        Ensures:
        - All required attributes are present.
        - parcel_id is unique and non-empty.
        - destination is valid (if valid_locations set provided).
        - weight is positive (> 0).
        - value is non-negative (>= 0).
        - priority is a positive integer (e.g., 1 is highest priority).
        - deadline is a positive number.
        """
        seen_ids: Set[str] = set()
        validated: List[Dict[str, Any]] = []

        for index, item in enumerate(parcels):
            if not isinstance(item, dict):
                raise ValueError(f"Parcel at index {index} is not a dictionary.")

            missing = cls.REQUIRED_FIELDS - set(item.keys())
            if missing:
                raise ValueError(f"Parcel at index {index} missing required fields: {missing}")

            parcel_id = str(item["parcel_id"]).strip()
            if not parcel_id:
                raise ValueError(f"Parcel at index {index} has an empty parcel_id.")
            if parcel_id in seen_ids:
                raise ValueError(f"Duplicate parcel_id detected: '{parcel_id}' at index {index}.")
            seen_ids.add(parcel_id)

            destination = str(item["destination"]).strip()
            if not destination:
                raise ValueError(f"Parcel '{parcel_id}' has an empty destination.")
            if valid_locations is not None and destination not in valid_locations:
                raise ValueError(f"Parcel '{parcel_id}' destination '{destination}' not in valid locations.")

            weight = item["weight"]
            if not isinstance(weight, (int, float)) or weight <= 0:
                raise ValueError(f"Parcel '{parcel_id}' has invalid weight {weight}; must be > 0.")

            value = item["value"]
            if not isinstance(value, (int, float)) or value < 0:
                raise ValueError(f"Parcel '{parcel_id}' has invalid value {value}; must be >= 0.")

            priority = item["priority"]
            if not isinstance(priority, int) or priority <= 0:
                raise ValueError(f"Parcel '{parcel_id}' has invalid priority {priority}; must be a positive integer.")

            deadline = item["deadline"]
            if not isinstance(deadline, (int, float)) or deadline <= 0:
                raise ValueError(f"Parcel '{parcel_id}' has invalid deadline {deadline}; must be > 0.")

            validated.append({
                "parcel_id": parcel_id,
                "destination": destination,
                "weight": int(weight) if isinstance(weight, int) or weight.is_integer() else weight,
                "value": int(value) if isinstance(value, int) or value.is_integer() else value,
                "priority": priority,
                "deadline": deadline,
            })

        return validated

    def prioritized(self) -> List[Dict[str, Any]]:
        """Return parcels sorted by delivery priority (ascending, 1 is highest) then deadline (earliest first)."""
        return sort_parcels(self.parcels)

    def total_weight(self) -> float:
        """Calculate total weight of all managed parcels."""
        return sum(parcel["weight"] for parcel in self.parcels)

    def total_value(self) -> float:
        """Calculate total value of all managed parcels."""
        return sum(parcel["value"] for parcel in self.parcels)
