import os
from typing import Optional

import yaml

import cim_to_linkml.linkml_model as linkml_model


def init_yaml_serializer():
    yaml.add_representer(type(None), represent_none)
    yaml.add_representer(frozenset, frozenset_representer)
    yaml.add_representer(linkml_model.Slot, linkml_namedtuple_representer)
    yaml.add_representer(linkml_model.Class, linkml_namedtuple_representer)
    yaml.add_representer(linkml_model.Enum, linkml_namedtuple_representer)
    yaml.add_representer(linkml_model.Schema, linkml_namedtuple_representer)
    yaml.add_representer(linkml_model.PermissibleValue, linkml_namedtuple_representer)


def represent_none(self, _):
    return self.represent_scalar("tag:yaml.org,2002:null", "")


def frozenset_representer(dumper, data):
    assert type(data) == frozenset
    if len(data) == 0:
        return dumper.represent_none(data)

    for el in data:  # Only check first element.
        if type(el) == tuple and len(el) == 2:
            return dumper.represent_dict(dict(data))
        else:
            return dumper.represent_set(data)


def linkml_namedtuple_representer(dumper, data):
    return dumper.represent_dict(data._asdict())


def write_schema(schema: linkml_model.Schema, out_file: Optional[os.PathLike | str] = None) -> None:
    if out_file is None:
        path_parts = schema.name.split(".")
        dir_path = os.path.join("schemas", os.path.sep.join(path_parts[:-1]))
        file_name = f"{path_parts[-1]}.yml"
        out_file = os.path.join(dir_path, file_name)
        os.makedirs(dir_path, exist_ok=True)

    with open(out_file, "w") as f:
        yaml.dump(schema, f, indent=2, default_flow_style=False, sort_keys=False)
