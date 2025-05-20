import os
from dataclasses import asdict

import yaml

from cim_to_linkml.cim18.linkml.class_.model import Class
from cim_to_linkml.cim18.linkml.enumeration.model import Enum, PermissibleValue
from cim_to_linkml.cim18.linkml.schema.model import Schema
from cim_to_linkml.cim18.linkml.slot.model import Slot


def init_yaml_serializer():
    yaml.add_representer(type(None), represent_none)
    yaml.add_representer(Slot, represent_linkml_slot)
    yaml.add_representer(Class, represent_linkml_class)
    yaml.add_representer(Enum, represent_linkml_enum)
    yaml.add_representer(PermissibleValue, represent_linkml_permissible_value)
    yaml.add_representer(Schema, represent_linkml_schema)


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
    d = {k: v for k, v in asdict(data).items() if k not in ["name"] if v not in [[], {}, None]}

    return dumper.represent_dict(d)


def represent_linkml_slot(dumper, data):
    d = {k: v for k, v in asdict(data).items() if k not in ["name"] if v not in [[], {}, None]}

    return dumper.represent_dict(d)


def write_schema(schema: Schema, out_file: os.PathLike | str) -> None:
    with open(out_file, "w") as f:
        yaml.dump(schema, f, indent=2, default_flow_style=False, sort_keys=False)
