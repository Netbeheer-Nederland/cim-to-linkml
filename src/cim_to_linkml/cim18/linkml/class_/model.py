from pydantic import Field

from cim_to_linkml.cim18.linkml.model import IRI, CURIE, SlotName, Element
from cim_to_linkml.cim18.linkml.slot.model import Slot


class Class(Element):
    class_uri: IRI | CURIE | None = Field(None)
    is_a: str | None = Field(None)
    attributes: dict[SlotName, Slot] | None = Field(None)