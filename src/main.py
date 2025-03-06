import sys
from collections import defaultdict, deque
from typing import Tuple, Dict, Hashable, Collection, TypeVar

from mbta_client import (
    get_subway_routes,
    get_subway_route_to_stops_mapping,
    get_subway_stop_to_routes_mapping,
    get_subway_routes_for_stop,
    get_subway_route_id_to_name_mapping,
    get_subway_stop_name_to_id_mapping,
)
from models import Route, Stop


def question_1() -> None:
    print("Subway Routes:")
    for route in get_subway_routes():
        print(f"\t{route.long_name}")


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


K = TypeVar("K", bound=Hashable)
V = TypeVar("V", bound=Collection)


def find_multi_value_items(mapping: Dict[K, V]) -> Dict[K, V]:
    return {k: v for k, v in mapping.items() if len(v) >= 2}


def question_2() -> None:
    """
    Extend your program so it displays the following additional information.
    1. The name of the subway route with the most stops as well as a count of its stops.
    2. The name of the subway route with the fewest stops as well as a count of its stops.
    3. A list of the stops that connect two or more subway routes along with the relevant route names for
    each of those stops.
    """

    (route_with_most, most_in_a_route), (route_with_least, least_in_a_route) = (
        find_longest_and_shortest_route(get_subway_route_to_stops_mapping())
    )

    print(
        f"Route with the most stops: {route_with_most.long_name} with {most_in_a_route} stops"
    )
    print(
        f"\nRoute with the least stops: {route_with_least.long_name} with {least_in_a_route} stops"
    )

    mapping = get_subway_stop_to_routes_mapping()
    multi_route_stops = find_multi_value_items(mapping)
    print("\nStops that connect multiple routes:")
    for stop, routes in sorted(multi_route_stops.items()):
        print(f"{stop.name}: {', '.join(sorted(r.long_name for r in routes))}")


def build_adjacency_list(
    stop_to_routes_mapping: dict[Stop, set[Route]],
) -> dict[str, set[str]]:
    adj_list = defaultdict(set)
    for routes in stop_to_routes_mapping.values():
        # if the stop has multiple routes then those routes are connected
        if len(routes) > 1:
            for route in routes:
                connected_route_ids = {r.id for r in routes} - {route.id}
                adj_list[route.id].update(connected_route_ids)

    return adj_list


def find_shortest_path(
    adj_list: dict[str, set[str]], start: str, end: str
) -> list[str] | None:
    """
    Function to find a shortest path between two vertices in a graph using breadth-first search.
    :param adj_list: An adjacency list for the graph of interest, mapping nodes to their respective sets of neighbors.
    :param start: starting vertex for the path
    :param end: ending vertex for the path
    :return: List of vertices in the path or None if no path exists.
    """
    # Using queue for O(1) operations
    edge_queue = deque([(start, [start])])
    visited = set[str]()

    while edge_queue:
        vertex, path = edge_queue.popleft()

        # if we reached the end, we have a shortest path
        if vertex == end:
            return path

        # If we haven't reached the end, explore the adjacent vertices
        for adjacent in adj_list[vertex]:
            if adjacent not in visited:
                # Add adjacent to our visited set so we don't loop or take longer paths
                visited.add(adjacent)
                edge_queue.append((adjacent, path + [adjacent]))

    # if we reach the end of the queue without a path, it's not possible
    return None


def find_viable_path(start_name: str, end_name: str) -> list[str] | None:
    """
    Determines a viable subway route between two stops, given their ids
    :param start_name: Name of starting stop.
    :param end_name: Name of destination stop.
    :return: List of route names forming the path, or None if no path exists.
    """
    name_to_id_mapping = get_subway_stop_name_to_id_mapping()
    start_id = name_to_id_mapping.get(start_name.title())
    end_id = name_to_id_mapping.get(end_name.title())

    if not start_id or not end_id:
        raise ValueError(
            f"I'm sorry, please pass in valid stop names to find the path: start is valid: {start_id is not None}, end is valid: {end_id is not None}"
        )

    routes_1 = get_subway_routes_for_stop(start_id)
    routes_2 = get_subway_routes_for_stop(end_id)

    if not (routes_1 and routes_2):
        raise ValueError("Routes not found for both stops.")

    # Direct connection check
    common_routes = routes_1.intersection(routes_2)
    if common_routes:
        return [next(iter(common_routes)).long_name]

    # Build route adjacency list
    adj_list = build_adjacency_list(get_subway_stop_to_routes_mapping())

    # Find a shortest path between routes
    path = find_shortest_path(
        adj_list, start=next(iter(routes_1)).id, end=next(iter(routes_2)).id
    )
    if not path:
        return None

    # Convert route IDs to names
    route_names = [
        get_subway_route_id_to_name_mapping().get(route_id) for route_id in path
    ]
    return route_names


if __name__ == "__main__":
    args = sys.argv[1:]  # Exclude the script name

    if len(args) == 3 and args[0] == "find_path":
        path = find_viable_path(args[1], args[2])
        if not path:
            print("No path found :(")
        else:
            print(f"Path from {args[1]} -> {args[2]}: {' -> '.join(path)}")
    elif args[0] == "question_1":
        print("Question 1:")
        question_1()
    elif args[0] == "question_2":
        print("\nQuestion 2:")
        question_2()
