import os
from collections import defaultdict
from functools import lru_cache

from dotenv import load_dotenv
from requests import get

from models import Route, Stop

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
        "sort": "long_name",
    }  # type 0 = Light Rail, type 1 = Heavy Rail
    headers = {"x-api-key": MBTA_API_KEY}
    response = get(url=url, params=params, headers=headers)
    response.raise_for_status()
    return [Route.from_json(item) for item in response.json()["data"]]


@lru_cache(maxsize=1)
def get_subway_stops() -> list[Stop]:
    url = f"{MBTA_API_BASE_URL}/stops"
    params = {
        "filter[route_type]": "0,1",
    }
    headers = {"x-api-key": MBTA_API_KEY}
    response = get(url=url, params=params, headers=headers)
    response.raise_for_status()
    return [Stop.from_json(item) for item in response.json()["data"]]


@lru_cache()
def get_stops_for_route(route_id: str) -> list[Stop]:
    url = f"{MBTA_API_BASE_URL}/stops"
    params = {"include": "route", "filter[route]": route_id}
    headers = {"x-api-key": MBTA_API_KEY}
    response = get(url=url, params=params, headers=headers)
    response.raise_for_status()
    return [Stop.from_json(item) for item in response.json()["data"]]


@lru_cache(maxsize=1)
def get_subway_route_to_stops_mapping() -> dict[Route, set[Stop]]:
    routes = get_subway_routes()
    return {r: set(get_stops_for_route(r.id)) for r in routes}


@lru_cache(maxsize=1)
def get_subway_stop_to_routes_mapping() -> dict[Stop, set[Route]]:
    stop_to_routes_mapping = defaultdict(set)
    for route, stops in get_subway_route_to_stops_mapping().items():
        for stop in stops:
            stop_to_routes_mapping[stop].add(route)

    return stop_to_routes_mapping


def get_subway_routes_for_stop(stop_id: str) -> set[Route]:
    url = f"{MBTA_API_BASE_URL}/routes"
    params = {"filter[type]": "0,1", "filter[stop]": stop_id}
    headers = {"x-api-key": MBTA_API_KEY}
    response = get(url=url, params=params, headers=headers)
    response.raise_for_status()
    return {Route.from_json(item) for item in response.json()["data"]}


def get_subway_route_id_to_name_mapping() -> dict[str, str]:
    routes = get_subway_routes()
    return {r.id: r.long_name for r in routes}


def get_subway_stop_name_to_id_mapping() -> dict[str, str]:
    stops = get_subway_stops()
    return {s.name: s.id for s in stops}
