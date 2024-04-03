from typing import NamedTuple, Optional


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
    enum_uri: Optional[str] = None
    description: Optional[str] = None
    permissible_values: frozenset[tuple[str, PermissibleValue]] = frozenset()


class Class(NamedTuple):
    name: str
    class_uri: Optional[str] = None
    is_a: Optional[str] = None
    description: Optional[str] = None
    attributes: frozenset[tuple[str, Slot]] = frozenset()


class Schema(NamedTuple):
    id: str
    name: str
    enums: frozenset[tuple[str, Enum]] = frozenset()
    classes: frozenset[tuple[str, Class]] = frozenset()
