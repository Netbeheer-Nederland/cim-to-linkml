from typing import NamedTuple, Optional

CIM_PREFIX = "cim"
CIM_BASE_URI = "https://cim.ucaiug.io/ns#"


class PermissibleValue(NamedTuple):
    text: str
    meaning: Optional[str] = None


class Slot(NamedTuple):
    name: str
    range: str
    required: bool = False
    multivalued: bool = False
    description: Optional[str] = None
    slot_uri: Optional[str] = None


class Enum(NamedTuple):
    name: str
    permissible_values: frozenset[tuple[str, PermissibleValue]]
    enum_uri: Optional[str] = None
    description: Optional[str] = None


class Class(NamedTuple):
    name: str
    attributes: Optional[frozenset[tuple[str, Slot]]] = None
    class_uri: Optional[str] = None
    is_a: Optional[str] = None
    description: Optional[str] = None


class Schema(NamedTuple):
    id: str
    name: str
    title: Optional[str] = None
    description: Optional[str] = None
    imports: Optional[list[str]] = None
    prefixes: Optional[dict[str, str]] = None
    default_curi_maps: Optional[list[str]] = None
    default_prefix: Optional[str] = None
    default_range: Optional[str] = None
    classes: Optional[frozenset[tuple[str, Class]]] = None
    enums: Optional[frozenset[tuple[str, Enum]]] = None
