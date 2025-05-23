from dataclasses import dataclass
from typing import Any

from cim_to_linkml.cim18.linkml.model import IRI, CURIE, SlotName, SubsetName
from cim_to_linkml.cim18.linkml.slot.model import Slot


@dataclass
class Class:
    name: str  # ID
    class_uri: IRI | CURIE | None = None
    is_a: str | None = None
    annotations: dict[str, Any] | None = None
    description: str | None = None
    attributes: dict[SlotName, Slot] | None = None
    subsets: list[SubsetName] | None = None