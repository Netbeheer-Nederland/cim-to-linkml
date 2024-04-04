import os
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Literal, NamedTuple, Optional
from itertools import groupby
from operator import attrgetter, itemgetter

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


### Utils.
def group_by(iterable, attr=None, item=None, singleton_groups=False) -> dict:
    if attr is not None:
        key = attrgetter(attr)
    elif item is not None:
        key = itemgetter(item)
    else:
        raise TypeError("Please supply either `item` or `attr`")

    return {
        name: next(group) if singleton_groups else list(group)
        for name, group in groupby(sorted(iterable, key=key), key)
    }


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


class Package(NamedTuple):
    id: ObjectID
    name: PackageName
    notes: Optional[str] = None
    author: Optional[str] = None
    created_date: datetime = datetime.now()
    modified_date: datetime = datetime.now()
    parent: Optional[ObjectID] = None


class Attribute(NamedTuple):
    id: AttributeID
    class_: ObjectID
    name: AttributeName
    lower_bound: CardinalityValue = 0
    upper_bound: CardinalityValue = 1
    type: Optional[
        ClassName
    ] = None  # `NULL` for enumeration values, a class name otherwise.
    default: Optional[str] = None
    notes: Optional[str] = None
    stereotype: Optional[AttributeStereotype] = None


class Class(NamedTuple):
    id: ObjectID
    name: ClassName
    package: ObjectID
    attributes: frozenset[Attribute]
    created_date: datetime = datetime.now()
    modified_date: datetime = datetime.now()
    author: Optional[str] = None
    note: Optional[str] = None
    stereotype: Optional[ClassStereotype] = None


class Relation(NamedTuple):
    id: ConnectorID
    type: RelationType
    source_class: ObjectID
    dest_class: ObjectID
    direction: Optional[RelationDirection] = None
    # sub_type: Optional[RelationSubType] = None
    source_card: Cardinality = Cardinality()
    source_role: Optional[str] = None
    source_role_note: Optional[str] = None
    dest_card: Cardinality = Cardinality()
    dest_role: Optional[str] = None
    dest_role_note: Optional[str] = None


class Classes:
    def __init__(self, classes):
        self.by_id = group_by(classes, attr="id", singleton_groups=True)
        self.by_name = group_by(classes, attr="name", singleton_groups=True)
        self.by_pkg_id = group_by(classes, attr="package", singleton_groups=False)


class Relations:
    def __init__(self, relations):
        self.by_id = group_by(relations, attr="id", singleton_groups=True)
        self.by_source_id = group_by(
            relations, attr="source_class", singleton_groups=False
        )
        self.by_dest_id = group_by(relations, attr="dest_class", singleton_groups=False)


class Packages:
    def __init__(self, packages):
        self.by_id = group_by(packages, attr="id", singleton_groups=True)


class Project:
    def __init__(
        self, packages: Packages, classes: Classes, relations: Relations
    ) -> None:
        self.packages = packages
        self.classes = classes
        self.relations = relations
