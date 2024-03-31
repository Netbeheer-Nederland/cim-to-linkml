from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Literal, Self, NamedTuple

ObjectID = int
ConnectorID = int
AttributeID = int
AttributeName = str
RelationName = str
ClassName = str
PackageName = str
CardinalityValue = int | Literal["*"]


class Cardinality(NamedTuple):
    lower_bound: CardinalityValue = 0
    upper_bound: CardinalityValue = 1


class RelationSubType(Enum):
    WEAK = "Weak"


class RelationDirection(Enum):
    SOURCE_TO_DESTINATION = "Source -> Destination"
    UNSPECIFIED = "Unspecified"
    BI_DIRECTIONAL = "Bi-Directional"


class RelationType(Enum):
    AGGREGATION = "Aggregation"
    ASSOCIATION = "Association"
    DEPENDENCY = "Dependency"
    GENERALIZATION = "Generalization"
    NOTELINK = "NoteLink"
    PACKAGE = "Package"


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
class Package:
    id: ObjectID
    name: PackageName
    author: str
    parent: Self
    created_date: datetime
    modified_date: datetime
    notes: str


@dataclass
class Attribute:
    id: AttributeID
    domain: "Class"
    name: AttributeName
    lower_bound: CardinalityValue
    upper_bound: CardinalityValue
    type: "Class"
    default: str | None
    notes: str | None
    stereotype: AttributeStereotype | None


@dataclass
class EnumerationValue(Attribute):
    stereotype = AttributeStereotype.ENUM


@dataclass
class Class:
    id: ObjectID
    name: ClassName
    author: str
    package: Package
    attributes: dict[AttributeName, Attribute]  # TODO: Make list?
    created_date: datetime
    modified_date: datetime
    note: str | None
    stereotype: ClassStereotype | None


# @dataclass
# class EnumerationClass(Class):
#     stereotype = ClassStereotype.ENUMERATION


# @dataclass
# class CIMDatatypeClass(Class):
#     stereotype = ClassStereotype.CIMDATATYPE


# @dataclass
# class PrimitiveClass(Class):
#     stereotype = ClassStereotype.PRIMITIVE


@dataclass
class Relation:
    id: ConnectorID
    connector_type: RelationType
    source_class: Class
    dest_class: Class
    direction: RelationDirection | None
    sub_type: RelationSubType | None
    source_card: Cardinality
    source_role: str | None
    source_role_note: str | None
    dest_card: Cardinality | None
    dest_role: str | None
    dest_role_note: str | None
