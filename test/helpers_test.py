from typing import Any

import pytest

from helpers import find_multi_value_items


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
