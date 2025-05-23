from dataclasses import dataclass
from enum import Enum

from cim_to_linkml.cim18.linkml.model import URI, CURIE


class PrimitiveType(Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATE = "date"
    DATETIME = "datetime"


class UCUMCode(Enum):
    DEG = "deg"
    ...  # TODO: Fill out.


class QuantityKind(Enum):
    ANGLEDEGREES = "cim:AngleDegrees"


class Symbol(Enum):
    ANG = "Å"


@dataclass
class Unit:
    symbol: Symbol
    ucum_code: UCUMCode
    has_quantity_kind: QuantityKind


@dataclass
class CIMDataType:
    name: str
    uri: URI | CURIE
    base: PrimitiveType
    required: bool = False
    description: str | None = None
    unit: Unit | None = None
