import os
from typing import Optional

import yaml

import cim_to_linkml.linkml_model as linkml_model


def init_yaml_serializer():
    yaml.add_representer(type(None), represent_none)
    yaml.add_representer(linkml_model.Slot, represent_linkml_slot)
    yaml.add_representer(linkml_model.Class, represent_linkml_class)
    yaml.add_representer(linkml_model.Enum, represent_linkml_enum)
    yaml.add_representer(linkml_model.Subset, represent_linkml_subset)
    yaml.add_representer(linkml_model.PermissibleValue, represent_linkml_permissible_value)
    yaml.add_representer(linkml_model.Schema, represent_linkml_schema)


def represent_none(self, _):
    """Replace `null` with the empty string."""

    return self.represent_scalar("tag:yaml.org,2002:null", "")


def represent_linkml_schema(dumper, data):
    d = {k: v for k, v in data._asdict().items() if v not in [[], {}, None]}

    for k, v in d.get("subsets", {}).items():
        if not v.description:
            d["subsets"][k] = None

    return dumper.represent_dict(d)


def represent_linkml_permissible_value(dumper, data):
    d = {k: v for k, v in data._asdict().items() if v is not None}

    return dumper.represent_dict(d)


def represent_linkml_subset(dumper, data):
    d = {k: v for k, v in data._asdict().items() if k not in ["name"] if v not in [[], {}, None]}

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


def write_schema(schema: linkml_model.Schema, out_file: Optional[os.PathLike | str] = None) -> None:
    if out_file is None:
        path_parts = schema.name.split(".")
        dir_path = os.path.join("schemas", os.path.sep.join(path_parts[:-1]))
        file_name = f"{path_parts[-1]}.yml"
        out_file = os.path.join(dir_path, file_name)
        os.makedirs(dir_path, exist_ok=True)

    with open(out_file, "w") as f:
        yaml.dump(schema, f, indent=2, default_flow_style=False, sort_keys=False)
