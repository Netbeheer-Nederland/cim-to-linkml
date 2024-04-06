import os
from typing import Optional

import yaml

import cim_to_linkml.linkml_model as linkml_model


def init_yaml_serializer():
    yaml.add_representer(type(None), represent_none)
    yaml.add_representer(linkml_model.Slot, linkml_namedtuple_representer(exclude_fields=["name"]))
    yaml.add_representer(linkml_model.Class, linkml_namedtuple_representer(exclude_fields=["name"]))
    yaml.add_representer(linkml_model.Enum, linkml_namedtuple_representer(exclude_fields=["name"]))
    yaml.add_representer(linkml_model.Subset, linkml_namedtuple_representer(exclude_fields=["name"]))
    yaml.add_representer(linkml_model.Schema, linkml_namedtuple_representer())
    yaml.add_representer(linkml_model.PermissibleValue, linkml_namedtuple_representer())


def represent_none(self, _):
    return self.represent_scalar("tag:yaml.org,2002:null", "")


def linkml_namedtuple_representer(exclude_fields: list[str] | None = None):
    def representer(dumper, data):
        d = data._asdict()

        if exclude_fields is not None:
            for k in exclude_fields:
                del d[k]

        empty_collection_fields = [k for k, v in d.items() if v in [[], {}]]
        for k in empty_collection_fields:
            del d[k]

        return dumper.represent_dict(d)

    return representer


def write_schema(schema: linkml_model.Schema, out_file: Optional[os.PathLike | str] = None) -> None:
    if out_file is None:
        path_parts = schema.name.split(".")
        dir_path = os.path.join("schemas", os.path.sep.join(path_parts[:-1]))
        file_name = f"{path_parts[-1]}.yml"
        out_file = os.path.join(dir_path, file_name)
        os.makedirs(dir_path, exist_ok=True)

    with open(out_file, "w") as f:
        yaml.dump(schema, f, indent=2, default_flow_style=False, sort_keys=False)
