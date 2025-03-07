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

    # Initialize variables using the first item
    iterator = iter(route_to_stops_mapping.items())
    first_route, first_stops = next(iterator)
    route_with_most = route_with_least = first_route
    most_in_a_route = least_in_a_route = len(first_stops)

    # Loop over the remaining items
    for route, stops in iterator:
        number_of_stops = len(stops)
        if number_of_stops > most_in_a_route:
            most_in_a_route = number_of_stops
            route_with_most = route
        elif number_of_stops < least_in_a_route:
            least_in_a_route = number_of_stops
            route_with_least = route

    return (route_with_most, most_in_a_route), (route_with_least, least_in_a_route)
