from dataclasses import dataclass

from cim_to_linkml.cim18.linkml.model import URI, CURIE, ClassName, EnumName, TypeName
from cim_to_linkml.cim18.linkml.type_.model import PrimitiveType


@dataclass
class Slot:
    name: str
    slot_uri: URI | CURIE
    range: PrimitiveType | TypeName | EnumName | ClassName
    required: bool = False
    multivalued: bool = False
    description: str | None = None