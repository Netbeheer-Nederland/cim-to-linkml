from pydantic import BaseModel, Field

from cim_to_linkml.cim18.linkml.model import IRI, CURIE, ClassName, EnumName, TypeName, Element
from cim_to_linkml.cim18.linkml.type_.model import PrimitiveType


class Slot(Element):
    slot_uri: IRI | CURIE | None = Field(None)
    range: PrimitiveType | TypeName | EnumName | ClassName
    required: bool = Field(False)
    multivalued: bool = Field(False)