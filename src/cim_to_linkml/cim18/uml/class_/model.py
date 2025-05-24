from collections import UserDict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from cim_to_linkml.cim18.uml.model import ObjectID
from cim_to_linkml.cim18.uml.multiplicity.model import Multiplicity

type AttributeID = int
type AttributeName = str
type ClassName = str


class ClassStereotype(Enum):
    NONE = None
    CIM_DATATYPE = "CIMDatatype"
    PRIMITIVE = "Primitive"
    ENUMERATION = "enumeration"
    COMPOUND = "Compound"


class AttributeStereotype(Enum):
    NONE = None
    ENUM = "enum"


@dataclass
class Attribute:
    class_: ObjectID
    id: AttributeID
    name: AttributeName
    type: ClassName | None  # Enumeration values have type `None`
    multiplicity: Multiplicity = field(default_factory=Multiplicity)
    default: str | None = None
    notes: str | None = None
    stereotype: AttributeStereotype = AttributeStereotype.NONE


class Attributes(UserDict[AttributeID, Attribute]):
    def by_name(self, name: str) -> Attribute | None:
        for attr_id, attr in self.items():
            if attr.name == name:
                return attr

        return None


@dataclass
class Class:
    id: ObjectID
    name: ClassName
    package: ObjectID
    attributes: Attributes
    created_date: datetime = datetime.now()
    modified_date: datetime = datetime.now()
    author: str | None = None
    note: str | None = None
    stereotype: ClassStereotype = ClassStereotype.NONE
