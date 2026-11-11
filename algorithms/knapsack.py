"""0/1 Knapsack optimization using Dynamic Programming.

Recurrence:
    Let DP[i][w] represent the maximum value achievable considering the first i items
    with remaining vehicle carrying capacity w.

    Base Case:
        DP[0][w] = 0  for all 0 <= w <= capacity
        DP[i][0] = 0  for all 0 <= i <= n

    Recurrence Step:
        If weight[i - 1] > w:
            DP[i][w] = DP[i - 1][w]
        Else:
            DP[i][w] = max(
                DP[i - 1][w],                                  # item i - 1 excluded
                DP[i - 1][w - weight[i - 1]] + value[i - 1]     # item i - 1 included
            )

Reconstruction:
    Backtrack from DP[n][capacity]:
    If DP[i][w] != DP[i - 1][w]:
        Item (i - 1) is selected.
        w = w - weight[i - 1]
    Else:
        Item (i - 1) is rejected.

Complexity:
    - Time Complexity: O(n * W)
    - Space Complexity: O(n * W) for the 2D DP table.
    where n is the number of parcels and W is the vehicle capacity.
"""

from typing import Any, Dict, List, Tuple


def knapsack_01(
    items: List[Dict[str, Any]],
    capacity: int,
    weight_key: str = "weight",
    value_key: str = "value",
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], int, int, List[List[int]]]:
    """Execute 0/1 Knapsack dynamic programming with full 2D table construction and item reconstruction.

    Args:
        items: List of item dictionaries.
        capacity: Maximum allowable vehicle capacity (must be integer >= 0).
        weight_key: Dictionary key for item weight.
        value_key: Dictionary key for item value/benefit.

    Returns:
        A tuple of:
            - selected_items: List of items chosen in optimal solution.
            - rejected_items: List of items not chosen.
            - total_weight: Total weight of selected items.
            - total_value: Maximum total value achievable within capacity.
            - dp_table: The full (n+1) x (capacity+1) dynamic programming table.
    """
    if capacity < 0:
        raise ValueError("Vehicle capacity must be non-negative (>= 0).")

    for index, item in enumerate(items):
        weight = item.get(weight_key)
        value = item.get(value_key)
        if weight is None or not isinstance(weight, (int, float)) or weight < 0:
            raise ValueError(f"Item at index {index} has invalid weight: {weight}")
        if value is None or not isinstance(value, (int, float)) or value < 0:
            raise ValueError(f"Item at index {index} has invalid value: {value}")

    n = len(items)
    cap = int(capacity)

    # 1. Build (n + 1) x (cap + 1) table initialized to 0
    dp_table: List[List[int]] = [[0] * (cap + 1) for _ in range(n + 1)]

    # 2. Fill DP table iteratively
    for i in range(1, n + 1):
        item_weight = int(items[i - 1][weight_key])
        item_value = int(items[i - 1][value_key])

        for w in range(cap + 1):
            if item_weight > w:
                dp_table[i][w] = dp_table[i - 1][w]
            else:
                exclude_val = dp_table[i - 1][w]
                include_val = dp_table[i - 1][w - item_weight] + item_value
                if include_val > exclude_val:
                    dp_table[i][w] = include_val
                else:
                    dp_table[i][w] = exclude_val

    # 3. Backtrack to reconstruct selected and rejected items
    selected_items: List[Dict[str, Any]] = []
    rejected_items: List[Dict[str, Any]] = []
    w = cap

    for i in range(n, 0, -1):
        if dp_table[i][w] != dp_table[i - 1][w]:
            selected_items.append(items[i - 1])
            w -= int(items[i - 1][weight_key])
        else:
            rejected_items.append(items[i - 1])

    # Reverse selected and rejected to preserve original order
    selected_items.reverse()
    rejected_items.reverse()

    total_weight = sum(int(item[weight_key]) for item in selected_items)
    total_value = dp_table[n][cap]

    return selected_items, rejected_items, total_weight, total_value, dp_table


def knapsack(
    items: List[Dict[str, Any]],
    capacity: int,
    weight_key: str = "weight",
    value_key: str = "value",
) -> Tuple[List[Dict[str, Any]], int]:
    """Backward-compatible wrapper returning (selected_items, total_value)."""
    selected, _, _, total_val, _ = knapsack_01(
        items=items,
        capacity=capacity,
        weight_key=weight_key,
        value_key=value_key,
    )
    return selected, total_val
