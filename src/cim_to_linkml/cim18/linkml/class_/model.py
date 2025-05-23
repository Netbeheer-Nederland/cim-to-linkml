from dataclasses import dataclass
from typing import Any

from cim_to_linkml.cim18.linkml.model import URI, CURIE, SlotName
from cim_to_linkml.cim18.linkml.slot.model import Slot


@dataclass
class Class:
    name: str  # ID
    class_uri: URI | CURIE | None = None
    is_a: str | None = None
    annotations: dict[str, Any] | None = None
    description: str | None = None
    attributes: dict[SlotName, Slot] | None = None