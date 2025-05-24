from pydantic import BaseModel, Field

from cim_to_linkml.cim18.linkml.model import IRI, CURIE, Element

type EnumValName = str


class PermissibleValue(BaseModel):
    meaning: IRI | CURIE | None = None


class Enum(Element):
    enum_uri: IRI | CURIE | None = Field(None)
    permissible_values: dict[EnumValName, dict[str, PermissibleValue]] | None = Field(None)