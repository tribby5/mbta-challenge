import pytest

from main import find_shortest_path, build_adjacency_list
from models import Stop, Route


@pytest.mark.parametrize(
    ("test_id", "graph", "start", "end", "expected"),
    [
        (
            "should return the node if start=end",
            {"a": {"b"}, "b": {"a"}},
            "a",  # start
            "a",  # end
            ["a"],  # expected
        ),
        (
            "should return the shortest of two possible paths",
            {
                "a": {"b", "c"},
                "b": {"a", "c"},
                "c": {"a", "b"},
            },
            "a",  # start
            "c",  # end
            ["a", "c"],  # expected
        ),
        (
            "should be able to traverse the adj list multiple levels",
            {"a": {"b"}, "b": {"a", "c"}, "c": {"b"}},
            "a",  # start
            "c",  # end
            ["a", "b", "c"],  # expected
        ),
    ],
)
def test_find_shortest_path(
    test_id: str,
    graph: dict[str, set[str]],
    start: str,
    end: str,
    expected: list[str] | None,
) -> None:
    actual = find_shortest_path(graph, start, end)
    assert actual == expected


@pytest.mark.parametrize(
    ("test_id", "stop_to_route_mapping", "expected"),
    [
        (
            "should return an empty dictionary if no stops share routes",
            {
                Stop(id="stop_a", name="A"): {Route(id="route_1", long_name="1")},
                Stop(id="stop_b", name="B"): {Route(id="route_2", long_name="2")},
            },
            {},  # expected
        ),
        (
            "should return a correct adj list when stops share routes",
            {
                Stop(id="stop_a", name="A"): {
                    Route(id="route_1", long_name="1"),
                    Route(id="route_2", long_name="2"),
                    Route(id="route_3", long_name="3"),
                },
                Stop(id="stop_b", name="B"): {
                    Route(id="route_2", long_name="2"),
                    Route(id="route_4", long_name="4"),
                },
            },  # input mapping
            {
                "route_1": {"route_2", "route_3"},
                "route_2": {"route_1", "route_3", "route_4"},
                "route_3": {"route_1", "route_2"},
                "route_4": {"route_2"},
            },  # expected
        ),
    ],
)
def test_adjacency_list(
    test_id: str,
    stop_to_route_mapping: dict[Stop, set[Route]],
    expected: dict[str, set[str]],
) -> None:
    actual = build_adjacency_list(stop_to_route_mapping)
    assert actual == expected
