from typing import NamedTuple, Optional

ClassName = str
EnumName = str
SlotName = str
EnumValName = str
SubsetName = str
URI = str
CURIE = str


CIM_PREFIX = "cim"
CIM_BASE_URI = "https://cim.ucaiug.io/ns#"


class PermissibleValue(NamedTuple):
    meaning: Optional[URI | CURIE] = None


class Slot(NamedTuple):
    name: str
    range: str
    required: bool = False
    multivalued: bool = False
    description: Optional[str] = None
    slot_uri: Optional[URI | CURIE] = None


class Enum(NamedTuple):
    name: str
    permissible_values: dict[EnumValName, PermissibleValue]
    enum_uri: Optional[URI | CURIE] = None
    description: Optional[str] = None
    in_subset: Optional[list[SubsetName]] = None


class Class(NamedTuple):
    name: str
    attributes: Optional[dict[SlotName, Slot]] = None
    class_uri: Optional[URI | CURIE] = None
    is_a: Optional[str] = None
    description: Optional[str] = None
    in_subset: Optional[list[SubsetName]] = None


class Subset(NamedTuple):
    name: str
    # title: Optional[str] = None
    description: Optional[str] = None


class Schema(NamedTuple):
    id: URI | CURIE
    name: str
    title: Optional[str] = None
    description: Optional[str] = None
    created_by: Optional[URI | CURIE] = None
    metamodel_version: Optional[str] = None
    imports: Optional[list[str]] = None
    prefixes: Optional[dict[str, str]] = None
    default_curi_maps: Optional[list[str]] = None
    default_prefix: Optional[str] = None
    default_range: Optional[str] = None
    classes: Optional[dict[ClassName, Class]] = None
    enums: Optional[dict[EnumName, Enum]] = None
    subsets: Optional[dict[SubsetName, Subset]] = None
