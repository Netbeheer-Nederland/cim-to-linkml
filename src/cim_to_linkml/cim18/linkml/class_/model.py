from dataclasses import dataclass

from cim_to_linkml.cim18.linkml.model import URI, CURIE
from cim_to_linkml.cim18.linkml.slot.model import SlotName, Slot

ClassName = str

@dataclass
class Class:
    name: str  # ID
    class_uri: URI | CURIE
    is_a: str | None = None
    annotations: dict[str, str] | None = None
    from_schema: URI | None = None
    description: str | None = None
    attributes: dict[SlotName, Slot] | None = None