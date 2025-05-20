from dataclasses import dataclass
from datetime import datetime

from cim_to_linkml.cim18.linkml.class_.model import Class, ClassName
from cim_to_linkml.cim18.linkml.enumeration.model import Enum, EnumName
from cim_to_linkml.cim18.linkml.model import URI, CURIE, CIM_BASE_URI

LINKML_METAMODEL_VERSION = "1.7.0"  # TODO: Modify.

GITHUB_BASE_URL = "https://github.com/"
GITHUB_REPO_URL = "https://github.com//cim-to-linkml"

SCHEMA_NAME = "CIM"  # TODO: Determine.
SCHEMA_ID = CIM_BASE_URI + SCHEMA_NAME  # TODO: Determine.


@dataclass
class Schema:
    id: URI | CURIE
    name: str
    title: str | None = None
    description: str | None = None
    contributors: list[URI | CURIE] | None = None
    created_by: URI | CURIE | None = None
    generation_date: datetime | None = None
    license: str | None = None
    metamodel_version: str | None = None
    imports: list[str] | None = None
    prefixes: dict[str, str] | None = None
    default_curi_maps: list[str] | None = None
    default_prefix: str | None = None
    default_range: str | None = None
    classes: dict[ClassName, Class] | None = None
    enums: dict[EnumName, Enum] | None = None