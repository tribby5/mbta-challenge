import os
import sys
from collections import defaultdict
from functools import lru_cache
from typing import Any

from dotenv import load_dotenv
from requests import get

from models import Stop, Route

load_dotenv(dotenv_path="./.secrets.env")
MBTA_API_KEY = os.getenv("MBTA_API_KEY")

MBTA_API_BASE_URL = "https://api-v3.mbta.com"


@lru_cache(maxsize=1)
def get_subway_routes() -> list[Route]:
    url = f"{MBTA_API_BASE_URL}/routes"
    """
    Note: filtering at the API layer versus locally for several reasons:
        1. Reduces the amount to load from the server (less network traffic) and less to process locally.
        2. Presumably, the database table has an index that makes it a faster operation
        for the API to do then locally.
    """

    params = {
        "filter[type]": "0,1",
        "sort": "-long_name",
    }  # type 0 = Light Rail, type 1 = Heavy Rail
    headers = {"x-api-key": MBTA_API_KEY}
    response = get(url=url, params=params, headers=headers)
    response.raise_for_status()
    return [Route.from_json(item) for item in response.json()["data"]]


@lru_cache()
def get_stops_for_route(route_id: str) -> list[Stop]:
    url = f"{MBTA_API_BASE_URL}/stops"
    params = {"include": "route", "filter[route]": route_id}
    headers = {"x-api-key": MBTA_API_KEY}
    response = get(url=url, params=params, headers=headers)
    response.raise_for_status()
    return [Stop.from_json(item) for item in response.json()["data"]]


def route_id_name_mapping() -> dict[str, str]:
    routes = get_subway_routes()
    return {r.id: r.long_name for r in routes}


def question_1() -> None:
    print("Subway Routes:")
    for route in get_subway_routes():
        print(route.long_name)


def question_2() -> None:
    """
    Extend your program so it displays the following additional information.
    1. The name of the subway route with the most stops as well as a count of its stops.
    2. The name of the subway route with the fewest stops as well as a count of its stops.
    3. A list of the stops that connect two or more subway routes along with the relevant route names for
    each of those stops.
    """

    # Get all the stops for each route -- have to make a call per route per API restrictions
    routes = get_subway_routes()
    stops_to_route_mapping = defaultdict(list)
    route_name_mapping = route_id_name_mapping()

    route_with_most_stops = ""
    most_stops_in_a_route = -1
    route_with_least_stops = ""
    least_stops_in_a_route = sys.maxsize
    # Collect information as we loop through for efficiency
    for route in routes:
        route_stops = get_stops_for_route(route.id)
        number_of_stops = len(route_stops)

        for stop in route_stops:
            stops_to_route_mapping[stop.name].append(stop.route_id)

        if number_of_stops > most_stops_in_a_route:
            most_stops_in_a_route = number_of_stops
            route_with_most_stops = route.id
        elif number_of_stops < least_stops_in_a_route:
            least_stops_in_a_route = number_of_stops
            route_with_least_stops = route.id

    print(
        f"Route with most stops: {route_name_mapping[route_with_most_stops]} with {most_stops_in_a_route} stops"
    )
    print(
        f"Route with least stops: {route_name_mapping[route_with_least_stops]} with {least_stops_in_a_route} stops"
    )

    print("Stops that connect multiple routes:")
    for stop, routes in stops_to_route_mapping.items():
        if len(routes) > 1:
            route_names = [route_name_mapping[route] for route in routes]
            print(f"\t{stop}: {', '.join(sorted(route_names))}")


if __name__ == "__main__":
    question_2()
