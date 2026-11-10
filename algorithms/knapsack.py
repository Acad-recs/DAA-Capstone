"""0/1 knapsack algorithm for courier capacity planning."""


def knapsack(items, capacity, weight_key="weight", value_key="priority"):
    """Return selected items and their total value within *capacity*."""
    if capacity < 0:
        raise ValueError("capacity must be non-negative")

    table = [0] * (capacity + 1)
    choices = [[] for _ in range(capacity + 1)]
    for item in items:
        weight = item[weight_key]
        value = item[value_key]
        if weight < 0:
            raise ValueError("item weights must be non-negative")
        for remaining in range(capacity, weight - 1, -1):
            candidate = table[remaining - weight] + value
            if candidate > table[remaining]:
                table[remaining] = candidate
                choices[remaining] = choices[remaining - weight] + [item]
    return choices[capacity], table[capacity]
