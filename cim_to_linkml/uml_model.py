import os
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Literal, NamedTuple, Optional
from itertools import groupby
from operator import attrgetter

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
    attributes: frozenset[Attribute]
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


class ProjectClasses:
    def __init__(self, classes):
        self._classes = classes
        self._by_id = classes
        self._by_name = {
            name: next(classes)
            for name, classes in groupby(
                sorted(self._classes.values(), key=attrgetter("name")), attrgetter("name")
            )
        }
        self._by_pkg_id = {
            pkg_id: list(classes)
            for pkg_id, classes in groupby(
                sorted(self._classes.values(), key=attrgetter("package")),
                attrgetter("package"),
            )
        }

    @property
    def by_id(self):
        return self._by_id

    @property
    def by_name(self):
        return self._by_name

    @property
    def by_pkg_id(self):
        return self._by_pkg_id


class ProjectRelations:
    def __init__(self, relations):
        self._relations = relations
        self._by_id = relations
        self._by_source_id = {
            source_id: list(rels)
            for source_id, rels in groupby(
                sorted(self._relations.values(), key=attrgetter("source_class")),
                attrgetter("source_class"),
            )
        }
        self._by_dest_id = {
            dest_id: list(rels)
            for dest_id, rels in groupby(
                sorted(self._relations.values(), key=attrgetter("dest_class")),
                attrgetter("dest_class"),
            )
        }

    @property
    def by_id(self):
        return self._by_id

    @property
    def by_source_id(self):
        return self._by_source_id

    @property
    def by_dest_id(self):
        return self._by_dest_id


@dataclass(frozen=True)
class Project:
    packages: dict[ObjectID, Package]
    classes: ProjectClasses
    relations: ProjectRelations
