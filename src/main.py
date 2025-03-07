import argparse
import sys

from mbta_client import (
    get_subway_routes,
    get_subway_route_to_stops_mapping,
    get_subway_stop_to_routes_mapping,
    get_subway_stop_name_to_id_mapping,
)
from path_finding import find_shortest_subway_path
from transit_system_info import find_longest_and_shortest_route
from helpers import find_multi_value_items


def question_1() -> None:
    """
    Write a program that retrieves data representing all, what we'll call "subway" routes: "Light Rail" (type 0) and “Heavy Rail” (type 1). The program should list their “long names” on the console.
    """
    print("Subway Routes:")
    for route in get_subway_routes():
        print(f" > {route.long_name}")


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

    # pretty print
    print(f"{'Stop':<25} Routes")
    for stop, routes in sorted(multi_route_stops.items()):
        print(f"{stop.name:<25} {', '.join(sorted(r.long_name for r in routes))}")


def handle_question_3_args(start_name: str, end_name: str) -> (str | None, str | None):
    """
    Helper to take the stop names as args and make sure they can be resolved to valid stop ids before trying to find a path.
    :param start_name: Name of the starting stop
    :param end_name:  Name fo the ending stop
    :return: Tuple of the ids, but either one could be None if an id wasn't found
    """
    name_to_id_mapping = get_subway_stop_name_to_id_mapping()
    start_id = name_to_id_mapping.get(start_name.title().strip())
    end_id = name_to_id_mapping.get(end_name.title().strip())
    return start_id, end_id


def question_3(args: argparse.Namespace) -> None:
    """
    Extend your program again such that the user can provide any two stops on the subway routes you listed for question 1.
    List a rail route you could travel to get from one stop to the other.
    """
    start, end = handle_question_3_args(args.start, args.end)
    if start is None or end is None:
        print(
            f"Unable to identify your requested stop(s): {args.start} is {'not' if start is None else ''} valid:, {args.end} is {'not' if end is None else ''} valid",
            file=sys.stderr,
        )
        sys.exit(2)

    path = find_shortest_subway_path(start, end)
    if path is None:
        print("I'm sorry, no viable path exists between those two subway stops")
    else:
        print(f"{args.start.title()} -> {args.end.title()}: {' -> '.join(path)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="MBTA CLI Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # question 1
    subparsers.add_parser("question-1", help="Returns the list of subway routes.")

    # question 2
    subparsers.add_parser(
        "question-2",
        help="Returns the longest and shortest subway routes as well as the list of stops that are used in multiple routes.",
    )

    # find path (question 3)
    parser_find_path = subparsers.add_parser(
        "find-path", help="Find a viable path of subway routes between two stops"
    )
    parser_find_path.add_argument(
        "--start", type=str, help="Name of the starting subway stop"
    )
    parser_find_path.add_argument(
        "--end", type=str, help="Name of the ending subway stop"
    )

    args = parser.parse_args()
    if args.command == "question-1":
        question_1()
    elif args.command == "question-2":
        question_2()
    elif args.command == "find-path":
        question_3(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
