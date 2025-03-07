from pydantic import BaseModel, ConfigDict


class Route(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    long_name: str

    def __lt__(self, other):
        return self.long_name < other.long_name

    # If implementing for production - could use OpenAPI spec generator for model instead: https://docs.pydantic.dev/latest/integrations/datamodel_code_generator/
    @classmethod
    def from_mbta_json(cls, data: dict):
        try:
            return cls(id=data["id"], long_name=data["attributes"]["long_name"])
        except KeyError as e:
            raise ValueError("Unexpected format returned from MBTA API") from e


class Stop(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    name: str

    def __lt__(self, other):
        return self.name < other.name

    # If implementing for production - could use OpenAPI spec generator for model instead: https://docs.pydantic.dev/latest/integrations/datamodel_code_generator/
    @classmethod
    def from_mbta_json(cls, data: dict):
        try:
            return cls(id=data["id"], name=data["attributes"]["name"])
        except KeyError as e:
            raise ValueError("Unexpected format returned from MBTA API") from e
