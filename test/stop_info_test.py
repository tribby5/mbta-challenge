from typing import Tuple, Any

import pytest

from main import find_longest_and_shortest_route, find_multi_value_items
from models import Route, Stop


@pytest.mark.parametrize(
    ("test_id", "route_to_stops_mapping", "expected"),
    [
        (
            "Should return None if no stops",
            {},
            None
        ),
        (
            "Should return the same route if only one route",
            {Route(id="route_1", long_name="1"): {Stop(id="stop_a", name="a")}},
            ((Route(id="route_1", long_name="1"), 1), (Route(id="route_1", long_name="1"), 1)) # expected
        ),
        (
            "Should return the correct result if two routes of different lengths",
            {
                Route(id="route_1", long_name="1"): {Stop(id="stop_a", name="a")},
                Route(id="route_2", long_name="2"): {Stop(id="stop_a", name="a"), Stop(id="stop_b", name="b")},
            },
            ((Route(id="route_2", long_name="2"), 2), (Route(id="route_1", long_name="1"), 1))
        )
    ]
)
def test_find_longest_and_shortest_route(test_id: str, route_to_stops_mapping: dict[Route, set[Stop]], expected: Tuple[Tuple[Route, int], Tuple[Route, int]] | None) -> None:
    actual = find_longest_and_shortest_route(route_to_stops_mapping)
    assert actual == expected


@pytest.mark.parametrize(
    ("test_id", "mapping", "expected"),
    [
        (
            "Should return an empty dictionary if no key has multiple values",
            {"a": [1]}, # input
            {} # expected
        ),
        (
            "Should return correct multi value items when they exist",
            {1: ["a", "b"], 2: ["c"], 3: ["d", "e"]}, # input
            {1: ["a", "b"], 3: ["d", "e"]} # expected
        )
    ]
)
def test_finding_multi_value_items(test_id: str, mapping: dict[Any, Any], expected: dict[Any, Any]) -> None:
    actual = find_multi_value_items(mapping)
    assert actual == expected