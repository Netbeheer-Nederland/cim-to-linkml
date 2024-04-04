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
