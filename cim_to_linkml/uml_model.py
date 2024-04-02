import os
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Literal, NamedTuple, Optional

ObjectID = int
ConnectorID = int
AttributeID = int
AttributeName = str
RelationName = str
ClassName = str
PackageName = str
Many = Literal["*"]
CardinalityValue = int | Many

QEAFile = os.PathLike | str


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


@dataclass(frozen=True)
class Package:
    id: ObjectID
    name: PackageName
    notes: Optional[str] = None
    author: Optional[str] = None
    created_date: datetime = datetime.now()
    modified_date: datetime = datetime.now()
    parent: Optional[ObjectID] = None


@dataclass(frozen=True)
class Attribute:
    id: AttributeID
    class_: ObjectID
    name: AttributeName
    lower_bound: Optional[CardinalityValue] = 0
    upper_bound: Optional[CardinalityValue] = 1
    type: Optional[ClassName] = None  # `NULL` for enumeration values, a class name otherwise.
    default: Optional[str] = None
    notes: Optional[str] = None
    stereotype: Optional[AttributeStereotype] = None


@dataclass(frozen=True)
class EnumerationValue(Attribute):
    stereotype = AttributeStereotype.ENUM


@dataclass(frozen=True)
class Class:
    id: ObjectID
    name: ClassName
    package: ObjectID
    attributes: dict[AttributeName, Attribute]  # TODO: Make list?
    created_date: datetime = datetime.now()
    modified_date: datetime = datetime.now()
    author: Optional[str] = None
    note: Optional[str] = None
    stereotype: Optional[ClassStereotype] = None


# @dataclass(frozen=True)
# class EnumerationClass(Class):
#     stereotype = ClassStereotype.ENUMERATION


# @dataclass(frozen=True)
# class CIMDatatypeClass(Class):
#     stereotype = ClassStereotype.CIMDATATYPE


# @dataclass(frozen=True)
# class PrimitiveClass(Class):
#     stereotype = ClassStereotype.PRIMITIVE


@dataclass(frozen=True)
class Relation:
    id: ConnectorID
    type: RelationType
    source_class: ObjectID
    dest_class: ObjectID
    direction: Optional[RelationDirection] = None
    # sub_type: Optional[RelationSubType] = None
    source_card: Optional[Cardinality] = None
    source_role: Optional[str] = None
    source_role_note: Optional[str] = None
    dest_card: Optional[Cardinality] = None
    dest_role: Optional[str] = None
    dest_role_note: Optional[str] = None


@dataclass(frozen=True)
class Project:
    packages: dict[ObjectID, Package]
    classes: dict[ObjectID, Class]
    relations: dict[ObjectID, Relation]
