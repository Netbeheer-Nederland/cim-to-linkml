import os

import yaml

import cim_to_linkml.cim18.linkml.model as linkml_model


def init_yaml_serializer():
    yaml.add_representer(type(None), represent_none)
    yaml.add_representer(linkml_model.Slot, represent_linkml_slot)
    yaml.add_representer(linkml_model.Class, represent_linkml_class)
    yaml.add_representer(linkml_model.Enum, represent_linkml_enum)
    yaml.add_representer(linkml_model.PermissibleValue, represent_linkml_permissible_value)
    yaml.add_representer(linkml_model.Schema, represent_linkml_schema)


def represent_none(self, _):
    """Replace `null` with the empty string."""

    return self.represent_scalar("tag:yaml.org,2002:null", "")


def represent_linkml_schema(dumper, data):
    d = {k: v for k, v in data._asdict().items() if v not in [[], {}, None]}

    return dumper.represent_dict(d)


def represent_linkml_permissible_value(dumper, data):
    d = {k: v for k, v in data._asdict().items() if v is not None}

    return dumper.represent_dict(d)


def represent_linkml_enum(dumper, data):
    d = {k: v for k, v in data._asdict().items() if k not in ["name"] if v not in [[], {}, None]}

    return dumper.represent_dict(d)


def represent_linkml_class(dumper, data):
    d = {k: v for k, v in data._asdict().items() if k not in ["name"] if v not in [[], {}, None]}

    return dumper.represent_dict(d)


def represent_linkml_slot(dumper, data):
    d = {k: v for k, v in data._asdict().items() if k not in ["name"] if v not in [[], {}, None]}

    return dumper.represent_dict(d)


def write_schema(schema: linkml_model.Schema, out_file: os.PathLike | str) -> None:
    with open(out_file, "w") as f:
        yaml.dump(schema, f, indent=2, default_flow_style=False, sort_keys=False)
