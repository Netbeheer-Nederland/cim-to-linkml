from dataclasses import dataclass
from enum import Enum

from cim_to_linkml.cim18.linkml.model import IRI, CURIE


class PrimitiveType(Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DOUBLE = "double"
    DATE = "date"
    DATETIME = "datetime"
    TIME = "time"
    IRI = "string"  # TODO: Custom type would be better, so we can even align it with a IRI IRI.


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
    uri: IRI | CURIE
    base: PrimitiveType
    required: bool = False
    description: str | None = None
    unit: Unit | None = None
