from dataclasses import dataclass

from cim_to_linkml.cim18.linkml.model import IRI, CURIE

type EnumValName = str


@dataclass
class PermissibleValue:
    meaning: IRI | CURIE | None = None


@dataclass
class Enum:
    name: str
    enum_uri: IRI | CURIE
    permissible_values: dict[EnumValName, dict[str, PermissibleValue]]
    description: str | None = None
    from_schema: IRI | None = None

