from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from cim_to_linkml.cim18.uml.multiplicity.model import MultiplicityBound
from cim_to_linkml.cim18.uml.type_.model import CIMPrimitive

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
    type: CIMPrimitive
    lower_bound: MultiplicityBound = 0
    upper_bound: MultiplicityBound = 1
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


