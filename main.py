import os
from difflib import restore

from dotenv import load_dotenv
from requests import get

load_dotenv(dotenv_path="./.secrets.env")
MBTA_API_KEY = os.getenv("MBTA_API_KEY")

MBTA_API_BASE_URL = "https://api-v3.mbta.com"


def question_1() -> None:
    url = f"{MBTA_API_BASE_URL}/routes"
    """
    Note: filtering at the API layer versus locally for several reasons:
        1. Reduces the amount to load from the server (less network traffic) and less to process locally.
        2. Presumably, the database table has an index that makes it a faster operation
        for the API to do then locally.
    """

    params = {"filter[type]": "0,1"}  # type 0 = Light Rail, type 1 = Heavy Rail
    headers = {"x-api-key": MBTA_API_KEY}
    response = get(url=url, params=params, headers=headers)
    response.raise_for_status()

    try:
        results = response.json()["data"]
        subway_routes = sorted({r["attributes"]["long_name"] for r in results})
    except KeyError as e:
        raise ValueError(
            "Unexpected format returned from MBTA API routes endpoint"
        ) from e

    print("Subway Routes:")
    for route in subway_routes:
        print(route)


if __name__ == "__main__":
    question_1()
