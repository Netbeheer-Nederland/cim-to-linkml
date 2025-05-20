import os
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from functools import cached_property, lru_cache
from itertools import groupby
from operator import attrgetter
from typing import Literal, Optional

type ObjectID = int
type ConnectorID = int
type AttributeID = int
type AttributeName = str
type RelationName = str
type ClassName = str
type PackageName = str
type CardinalityValue = int | Literal["*"]
type QEAFile = os.PathLike | str


INFORMAL_PACKAGES = [
    29,
    30,
    31,
    32,
    50,
    54,
    59,
    60,
    62,
    64,
    66,
    71,
    75,
    76,
    88,
    92,
    94,
    99,
    100,
    132,
    133,
    134,
    135,
    136,
    137,
    138,
    139,
    140,
    142,
    143,
    144,
    160,
    188,
    195,
    224,
]

DOCUMENTATION_PACKAGES = [5, 27, 49, 70, 104, 189]


@dataclass
class Cardinality:
    lower_bound: CardinalityValue = 0
    upper_bound: CardinalityValue = 1


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
    notes: Optional[str] = None
    author: Optional[str] = None
    created_date: datetime = datetime.now()
    modified_date: datetime = datetime.now()
    parent: Optional[ObjectID] = None
    is_informal: bool = False
    is_documentation: bool = False


@dataclass
class Attribute:
    id: AttributeID
    class_: ObjectID
    name: AttributeName
    lower_bound: CardinalityValue = 0
    upper_bound: CardinalityValue = 1
    type: Optional[ClassName] = None  # `NULL` for enumeration values, a class name otherwise.
    default: Optional[str] = None
    notes: Optional[str] = None
    stereotype: Optional[AttributeStereotype] = None


@dataclass
class Class:
    id: ObjectID
    name: ClassName
    package: ObjectID
    attributes: dict[AttributeID, Attribute]
    created_date: datetime = datetime.now()
    modified_date: datetime = datetime.now()
    author: Optional[str] = None
    note: Optional[str] = None
    stereotype: Optional[ClassStereotype] = None


@dataclass
class Relation:
    id: ConnectorID
    type: RelationType
    source_class: ObjectID
    dest_class: ObjectID
    direction: Optional[RelationDirection] = None
    source_card: Cardinality = field(default_factory=Cardinality)
    source_role: Optional[str] = None
    source_role_note: Optional[str] = None
    dest_card: Cardinality = field(default_factory=Cardinality)
    dest_role: Optional[str] = None
    dest_role_note: Optional[str] = None


class Classes:
    def __init__(self, classes):
        self._data = classes

    @cached_property
    def by_id(self):
        return {c.id: c for c in sorted(self._data, key=attrgetter("id"))}

    @cached_property
    def by_name(self):
        key = attrgetter("name")

        classes_by_name = {}
        for name, classes in groupby(sorted(self._data, key=key), key=key):
            classes = list(sorted(classes, key=attrgetter("id")))
            class_ = classes[0]
            if len(classes) > 1:
                print(
                    f"Multiple classes with name {name}. Choosing one (object ID: {class_[0]}) "
                    f"and skipping the others (object IDs: {', '.join(str(c.id) for c in classes[1:])})."
                )
            classes_by_name[name] = class_

        return classes_by_name

    @cached_property
    def by_package(self):
        key = attrgetter("package")

        classes_by_package = {}
        for package_id, classes in groupby(sorted(self._data, key=key), key=key):
            classes = list(sorted(classes, key=attrgetter("id")))
            classes_by_package[package_id] = classes

        return classes_by_package


class Relations:
    def __init__(self, relations):
        self._data = relations

    @cached_property
    def by_id(self):
        return {r.id: r for r in sorted(self._data, key=attrgetter("id"))}

    @cached_property
    def by_source_class(self):
        key = attrgetter("source_class")

        relations_by_source_class = {}
        for source_class, relations in groupby(sorted(self._data, key=key), key=key):
            relations = list(sorted(relations, key=attrgetter("id")))
            relations_by_source_class[source_class] = relations

        return relations_by_source_class

    @cached_property
    def by_dest_class(self):
        key = attrgetter("dest_class")

        relations_by_dest_class = {}
        for dest_class, relations in groupby(sorted(self._data, key=key), key=key):
            relations = list(sorted(relations, key=attrgetter("id")))
            relations_by_dest_class[dest_class] = relations

        return relations_by_dest_class


class Packages:
    def __init__(self, packages):
        self._data = packages

    @cached_property
    def by_id(self):
        return {p.id: p for p in sorted(self._data, key=attrgetter("id"))}

    @cached_property
    def by_qualified_name(self):
        return {self.get_qualified_name(p_id): p for p_id, p in self.by_id.items()}

    @lru_cache(maxsize=173)
    def get_qualified_name(self, package_id):
        return ".".join(self._get_package_path(package_id))

    def _get_package_path(self, start_pkg_id, package_path=None):
        if package_path is None:
            package_path = []

        package = self.by_id[start_pkg_id]

        if package.parent in (0, None):
            return package_path

        return self._get_package_path(package.parent, [package.name] + package_path)


@dataclass
class Project:
    packages: dict[ObjectID, Package]
    classes: dict[ObjectID, Class]
    relations: dict[ObjectID, Relation]
