import sys
from typing import Tuple

from models import Route, Stop


def find_longest_and_shortest_route(
    route_to_stops_mapping: dict[Route, set[Stop]],
) -> Tuple[Tuple[Route, int], Tuple[Route, int]] | None:
    """
    Function to find the longest and shortest route and their length given a mapping
    :param route_to_stops_mapping: Mapping of the route to their individual stops
    :return: a tuple containing two tuples, the first with the longest route its length and the second with the same info for the shortest route
    """
    if not route_to_stops_mapping:
        return None

    route_with_most = None
    most_in_a_route = -1
    route_with_least = None
    least_in_a_route = sys.maxsize
    # Collect information as we loop through for efficiency
    for route, stops in route_to_stops_mapping.items():
        number_of_stops = len(stops)
        if number_of_stops > most_in_a_route:
            most_in_a_route = number_of_stops
            route_with_most = route
        if number_of_stops < least_in_a_route:
            least_in_a_route = number_of_stops
            route_with_least = route

    return (route_with_most, most_in_a_route), (route_with_least, least_in_a_route)
