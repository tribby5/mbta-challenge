from typing import TypeVar, Hashable, Collection, Dict

K = TypeVar("K", bound=Hashable)
V = TypeVar("V", bound=Collection)


def find_multi_value_items(mapping: Dict[K, V]) -> Dict[K, V]:
    """
    Generic helper function for filtering a dictionary to only items with multiple values.
    :param mapping: dictionary to filter
    :return: filtered dictionary - returns a new dictionary, not editing in place
    """
    return {k: v for k, v in mapping.items() if len(v) >= 2}
