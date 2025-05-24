import os
from typing import Any

import yaml
from pydantic import BaseModel

from cim_to_linkml.cim18.linkml.class_.model import Class as LinkMLClass
from cim_to_linkml.cim18.linkml.enumeration.model import Enum as LinkMLEnum, PermissibleValue as LinkMLPermissibleValue
from cim_to_linkml.cim18.linkml.schema.model import Schema as LinkMLSchema
from cim_to_linkml.cim18.linkml.slot.model import Slot as LinkMLSlot
from cim_to_linkml.cim18.linkml.type_.model import (
    CIMDataType as LinkMLCIMDataType,
    PrimitiveType as LinkMLPrimitiveType,
)


def order_dict(d: dict[str, Any], ordered_fields: list[str]) -> dict[str, Any]:
    if not set(d.keys()).issubset(set(ordered_fields)):
        raise ValueError("Make sure to provide an order for at least all present fields.")

    return {k: d[k] for k in ordered_fields if k in d}


def dump_model(obj: BaseModel) -> dict[str, Any]:
    return {k: getattr(obj, k) for k in obj.model_fields}


def remove_from_dict_if_falsey(d: dict[str, Any], *keys: str) -> dict[str, Any]:
    return {k: v for k, v in d.items() if (k not in keys) or (k in keys and bool(v))}


class SafeDumperNoAlias(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


def init_yaml_serializer():
    yaml.add_representer(type(None), represent_none, Dumper=SafeDumperNoAlias)
    yaml.add_representer(LinkMLSlot, represent_linkml_slot, Dumper=SafeDumperNoAlias)
    yaml.add_representer(LinkMLClass, represent_linkml_class, Dumper=SafeDumperNoAlias)
    yaml.add_representer(LinkMLCIMDataType, represent_linkml_cim_datatype, Dumper=SafeDumperNoAlias)
    yaml.add_representer(LinkMLPrimitiveType, represent_linkml_primitive_type, Dumper=SafeDumperNoAlias)
    yaml.add_representer(LinkMLEnum, represent_linkml_enum, Dumper=SafeDumperNoAlias)
    yaml.add_representer(LinkMLPermissibleValue, represent_linkml_permissible_value, Dumper=SafeDumperNoAlias)
    yaml.add_representer(LinkMLSchema, represent_linkml_schema, Dumper=SafeDumperNoAlias)


def represent_none(self, _):
    """Replace `null` with the empty string."""

    return self.represent_scalar("tag:yaml.org,2002:null", "")


def represent_linkml_primitive_type(dumper, val):
    return dumper.represent_scalar("tag:yaml.org,2002:str", str(val.value))


def represent_linkml_schema(dumper, data):
    schema_dict = order_dict(
        dump_model(data),
        [
            "id",
            "name",
            "title",
            "description",
            "created_by",
            "generation_date",
            "license",
            "metamodel_version",
            "contributors",
            "annotations",
            "imports",
            "default_curie_maps",
            "prefixes",
            "default_prefix",
            "default_range",
            "classes",
            "slots",
            "enums",
            "types",
            "subsets",
            "in_subset",
        ],
    )

    schema_dict = remove_from_dict_if_falsey(
        schema_dict,
        "title",
        "description",
        "created_by",
        "generation_date",
        "license",
        "metamodel_version",
        "contributors",
        "annotations",
        "imports",
        "default_curie_maps",
        "prefixes",
        "default_prefix",
        "default_range",
        "classes",
        "slots",
        "enums",
        "types",
        "in_subset",
        "subsets",
    )

    return dumper.represent_dict(schema_dict)


def represent_linkml_permissible_value(dumper, data):
    d = {k: v for k, v in dump_model(data).items() if v is not None}

    return dumper.represent_dict(d)


def represent_linkml_enum(dumper, data):
    d = {k: v for k, v in dump_model(data).items() if k not in ["name"] if v not in [[], {}, None]}

    return dumper.represent_dict(d)


def represent_linkml_class(dumper, data):
    d = {}
    for field, value in dump_model(data).items():
        if field == "name":
            continue
        elif field in ["class_uri", "is_a"] and value is None:
            continue
        # elif field == "attributes":
        #     d[field] = {attr.name: represent_linkml_slot(dumper, attr) for attr in value.values()}
        else:
            d[field] = value

    return dumper.represent_dict(d)


def represent_linkml_cim_datatype(dumper, data):
    d = {k: v for k, v in dump_model(data).items() if k not in ["name"] if v not in [[], {}, None]}

    return dumper.represent_dict(d)


def represent_linkml_slot(dumper, data):
    d = {k: v for k, v in dump_model(data).items() if k not in ["name"] if v not in [[], {}, None]}

    return dumper.represent_dict(d)


def write_schema(schema: LinkMLSchema, out_file: os.PathLike | str) -> None:
    with open(out_file, "w") as f:
        yaml.dump(schema, f, SafeDumperNoAlias, indent=2, default_flow_style=False, sort_keys=False)
