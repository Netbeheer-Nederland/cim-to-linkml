from dataclasses import dataclass

from cim_to_linkml.cim18.linkml.model import URI, CURIE

EnumName = str
EnumValName = str


@dataclass
class PermissibleValue:
    meaning: URI | CURIE | None = None


@dataclass
class Enum:
    name: str
    enum_uri: URI | CURIE
    permissible_values: dict[EnumValName, dict[str, PermissibleValue]]
    description: str | None = None
    from_schema: URI | None = None

