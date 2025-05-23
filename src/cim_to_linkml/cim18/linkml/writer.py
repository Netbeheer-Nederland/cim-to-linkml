import os
from dataclasses import is_dataclass, fields

import yaml

from cim_to_linkml.cim18.linkml.class_.model import Class as LinkMLClass
from cim_to_linkml.cim18.linkml.enumeration.model import Enum as LinkMLEnum, PermissibleValue as LinkMLPermissibleValue
from cim_to_linkml.cim18.linkml.schema.model import Schema as LinkMLSchema
from cim_to_linkml.cim18.linkml.slot.model import Slot as LinkMLSlot


def asdict(obj):
    # Non-recursive version of `dataclasses.asdict`.
    # This prevents slots from being turned into dictionaries before its representer
    # gets a chance to ever see it.

    if not is_dataclass(obj):
        raise TypeError("`asdict_non_recursive` should only be called on dataclass instances")
    return {f.name: getattr(obj, f.name) for f in fields(obj)}



def init_yaml_serializer():
    yaml.add_representer(type(None), represent_none)
    yaml.add_representer(LinkMLSlot, represent_linkml_slot)
    yaml.add_representer(LinkMLClass, represent_linkml_class)
    yaml.add_representer(LinkMLEnum, represent_linkml_enum)
    yaml.add_representer(LinkMLPermissibleValue, represent_linkml_permissible_value)
    yaml.add_representer(LinkMLSchema, represent_linkml_schema)


def represent_none(self, _):
    """Replace `null` with the empty string."""

    return self.represent_scalar("tag:yaml.org,2002:null", "")


def represent_linkml_schema(dumper, data):
    d = {k: v for k, v in asdict(data).items() if v not in [[], {}, None]}

    return dumper.represent_dict(d)


def represent_linkml_permissible_value(dumper, data):
    d = {k: v for k, v in asdict(data).items() if v is not None}

    return dumper.represent_dict(d)


def represent_linkml_enum(dumper, data):
    d = {k: v for k, v in asdict(data).items() if k not in ["name"] if v not in [[], {}, None]}

    return dumper.represent_dict(d)


def represent_linkml_class(dumper, data):
    d = {}
    for field, value in asdict(data).items():
        if field == "name":
            continue
        elif field in ["class_uri", "is_a"] and value is None:
            continue
        # elif field == "attributes":
        #     d[field] = {attr.name: represent_linkml_slot(dumper, attr) for attr in value.values()}
        else:
            d[field] = value

    return dumper.represent_dict(d)


def represent_linkml_slot(dumper, data):
    d = {k: v for k, v in asdict(data).items() if k not in ["name"] if v not in [[], {}, None]}

    return dumper.represent_dict(d)


def write_schema(schema: LinkMLSchema, out_file: os.PathLike | str) -> None:
    with open(out_file, "w") as f:
        yaml.dump(schema, f, indent=2, default_flow_style=False, sort_keys=False)
