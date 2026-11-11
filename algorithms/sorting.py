"""Merge Sort implementation and parcel prioritization policies.

Complexity:
- Time Complexity: O(n log n) in all cases (best, average, worst).
- Auxiliary Space: O(n) for merging subarrays.
- Stable: Yes (elements with equal keys retain their original relative order).
"""

from typing import Any, Callable, Dict, List, Optional, Tuple


def merge_sort(
    items: List[Any],
    key: Optional[Callable[[Any], Any]] = None,
    reverse: bool = False,
) -> List[Any]:
    """Sort a list of items using stable Merge Sort.

    Args:
        items: List of elements to sort.
        key: A function of one argument that extracts a comparison key from each element.
             If None, elements are compared directly.
        reverse: If True, elements are sorted in descending order.

    Returns:
        A new sorted list containing all elements from `items`.
    """
    if len(items) <= 1:
        return list(items)

    middle = len(items) // 2
    left = merge_sort(items[:middle], key=key, reverse=reverse)
    right = merge_sort(items[middle:], key=key, reverse=reverse)

    return _merge(left, right, key=key, reverse=reverse)


def _merge(
    left: List[Any],
    right: List[Any],
    key: Optional[Callable[[Any], Any]] = None,
    reverse: bool = False,
) -> List[Any]:
    """Merge two sorted lists stably."""
    result: List[Any] = []
    left_index = right_index = 0
    left_len, right_len = len(left), len(right)

    while left_index < left_len and right_index < right_len:
        val_left = key(left[left_index]) if key else left[left_index]
        val_right = key(right[right_index]) if key else right[right_index]

        if not reverse:
            # For ascending, maintain stability with <=
            if val_left <= val_right:
                result.append(left[left_index])
                left_index += 1
            else:
                result.append(right[right_index])
                right_index += 1
        else:
            # For descending, maintain stability with >=
            if val_left >= val_right:
                result.append(left[left_index])
                left_index += 1
            else:
                result.append(right[right_index])
                right_index += 1

    result.extend(left[left_index:])
    result.extend(right[right_index:])
    return result


def sort_parcels(parcels: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Sort parcels according to academic courier policy:
    1. Higher priority first (priority rank 1 is highest priority).
    2. Earlier deadline first (smaller deadline value is earlier).
    3. Tie-breaker: parcel_id ascending for deterministic output.

    Ordering Key:
        (priority, deadline, parcel_id)
    """
    def parcel_order_key(parcel: Dict[str, Any]) -> Tuple[int, float, str]:
        return (
            parcel.get("priority", 999),
            parcel.get("deadline", float("inf")),
            str(parcel.get("parcel_id", "")),
        )

    return merge_sort(parcels, key=parcel_order_key, reverse=False)
