from enum import Enum

from pydantic import BaseModel, Field

from cim_to_linkml.cim18.linkml.model import IRI, CURIE, Element


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


class Unit(BaseModel):
    symbol: Symbol | None = Field(None)
    ucum_code: UCUMCode | None = Field(None)
    has_quantity_kind: QuantityKind | None = Field(None)


class Type(Element):
    uri: IRI | CURIE | None = Field(None)
    typeof: PrimitiveType | None = Field(None)
    unit: Unit | None = Field(None)


class CIMDataType(Type):
    pass
