from pydantic import BaseModel


class Route(BaseModel):
    id: str
    long_name: str

    @classmethod
    def from_json(cls, data: dict):
        try:
            return cls(id=data["id"], long_name=data["attributes"]["long_name"])
        except KeyError as e:
            raise ValueError("Unexpected format returned from MBTA API") from e


class Stop(BaseModel):
    id: str
    name: str
    route_id: str

    @classmethod
    def from_json(cls, data: dict):
        try:
            return cls(
                id=data["id"],
                name=data["attributes"]["name"],
                route_id=data["relationships"]["route"]["data"]["id"],
            )
        except KeyError as e:
            raise ValueError("Unexpected format returned from MBTA API") from e
