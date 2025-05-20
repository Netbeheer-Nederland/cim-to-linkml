from dataclasses import dataclass

from cim_to_linkml.cim18.linkml.model import URI, CURIE

type SlotName = str


@dataclass
class Slot:
    name: str
    slot_uri: URI | CURIE
    range: str
    required: bool = False
    multivalued: bool = False
    description: str | None = None
