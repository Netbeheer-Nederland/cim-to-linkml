from datetime import datetime

from pydantic import Field

from cim_to_linkml.cim18.linkml.class_.model import Class
from cim_to_linkml.cim18.linkml.enumeration.model import Enum
from cim_to_linkml.cim18.linkml.model import IRI, CURIE, CIM_BASE_URI, ClassName, SlotName, EnumName, TypeName, Element
from cim_to_linkml.cim18.linkml.slot.model import Slot
from cim_to_linkml.cim18.linkml.type_.model import CIMDataType

LINKML_METAMODEL_VERSION = "1.7.0"  # TODO: Modify.

GITHUB_BASE_URL = "https://github.com/"
GITHUB_REPO_URL = "https://github.com//cim-to-linkml"

SCHEMA_NAME = "CIM"  # TODO: Determine.
SCHEMA_ID = CIM_BASE_URI + SCHEMA_NAME  # TODO: Determine.


class Schema(Element):
    id: IRI | CURIE = Field(...)
    name: str = Field(...)
    title: str | None = Field(None)
    contributors: list[IRI | CURIE] | None = Field(None)
    created_by: IRI | CURIE | None = Field(None)
    generation_date: datetime = Field(default_factory=datetime.now)
    license: str | None = Field(None)
    metamodel_version: str | None = Field(None)
    imports: list[str] | None = Field(None)
    prefixes: dict[str, str] | None = Field(None)
    default_curie_maps: list[str] | None = Field(None)
    default_prefix: str | None = Field(None)
    default_range: str | None = Field(None)
    classes: dict[ClassName, Class] | None = Field(None)
    enums: dict[EnumName, Enum] | None = Field(None)
    types: dict[TypeName, CIMDataType] | None = Field(None)
    slots: dict[SlotName, Slot] | None = Field(None)