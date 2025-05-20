from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from cim_to_linkml.cim18.uml.multiplicity.model import MultiplicityBound

type ObjectID = int
type AttributeID = int
type AttributeName = str
type ClassName = str


class ClassStereotype(Enum):
    CIMDATATYPE = "CIMDatatype"
    PRIMITIVE = "Primitive"
    ENUMERATION = "enumeration"
    COMPOUND = "Compound"
    IMAGE = "Image"


class AttributeStereotype(Enum):
    ENUM = "enum"
    DEPRECATED = "deprecated"


@dataclass
class Attribute:
    id: AttributeID
    class_: ObjectID
    name: AttributeName
    lower_bound: MultiplicityBound = 0
    upper_bound: MultiplicityBound = 1
    type: ClassName | None = None  # `NULL` for enumeration values, a class name otherwise.
    default: str | None = None
    notes: str | None = None
    stereotype: AttributeStereotype | None = None


@dataclass
class Class:
    id: ObjectID
    name: ClassName
    package: ObjectID
    attributes: dict[AttributeID, Attribute]
    created_date: datetime = datetime.now()
    modified_date: datetime = datetime.now()
    author: str | None = None
    note: str | None = None
    stereotype: ClassStereotype | None = None


