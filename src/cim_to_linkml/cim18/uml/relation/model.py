from dataclasses import dataclass, field
from enum import Enum

from cim_to_linkml.cim18.uml.model import ObjectID
from cim_to_linkml.cim18.uml.multiplicity.model import Multiplicity

type ConnectorID = int


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


@dataclass
class Relation:
    id: ConnectorID
    type: RelationType
    source_class: ObjectID
    dest_class: ObjectID
    direction: RelationDirection | None = None
    source_role: str | None = None
    source_role_note: str | None = None
    source_card: Multiplicity = field(default_factory=Multiplicity)
    dest_card: Multiplicity = field(default_factory=Multiplicity)
    dest_role: str | None = None
    dest_role_note: str | None = None
