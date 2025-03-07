from collections import defaultdict, deque

from mbta_client import (
    get_subway_routes_for_stop,
    get_subway_stop_to_routes_mapping,
    get_subway_route_id_to_name_mapping,
)
from models import Stop, Route


def build_adjacency_list(
    stop_to_routes_mapping: dict[Stop, set[Route]],
) -> dict[str, set[str]]:
    """
    Translates a subway stop to route mapping dictionary into an adjacency list of the routes to be used for graph functions.
    Two routes are "adjacent" if there exists at least one stop that is used by both routes.
    :param stop_to_routes_mapping: Mapping of stop to its set of route(s)
    :return: dictionary mapping a route id to the set of ids of its adjacent routes
    """
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


def find_shortest_subway_path(start_id: str, end_id: str) -> list[str] | None:
    """
    Determines a viable subway route between two stops, given their ids
    :param start_name: Name of starting stop.
    :param end_name: Name of destination stop.
    :return: List of route names forming the path, or None if no path exists.
    """
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
