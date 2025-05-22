from dataclasses import dataclass

from cim_to_linkml.cim18.linkml.model import URI, CURIE
from cim_to_linkml.cim18.linkml.type_.model import Type, PrimitiveType

type SlotName = str


@dataclass
class Slot:
    name: str
    slot_uri: URI | CURIE
    range: PrimitiveType | Type
    required: bool = False
    multivalued: bool = False
    description: str | None = None