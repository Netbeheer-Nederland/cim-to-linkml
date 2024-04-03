import yaml
from pprint import pprint
from itertools import groupby
from operator import itemgetter
import sqlite3
import cProfile
from dataclasses import dataclass
from typing import NamedTuple, Optional

from linkml_runtime.utils.schema_as_dict import schema_as_yaml_dump

import cim_to_linkml.uml_model as uml_model
import cim_to_linkml.linkml_model as linkml_model
from cim_to_linkml.read import read_uml_classes, read_uml_relations, read_uml_packages
from cim_to_linkml.parser import parse_uml_package, parse_uml_class, parse_uml_relation
from cim_to_linkml.generator import (
    gen_schema,
    get_super_class,
    get_rel_type_classes,
    _gen_class_deps,
    uml_project,
)

# def main():
#     db_file = "data/iec61970cim17v40_iec61968cim13v13b_iec62325cim03v17b_CIM100.1.1.1.qea"

#     with sqlite3.connect(db_file) as conn:
#         uml_class_results = read_uml_classes(conn)
#         uml_relation_results = read_uml_relations(conn)
#         uml_package_results = read_uml_packages(conn)

#     uml_packages = {pkg_row["id"]: parse_uml_package(pkg_row) for pkg_row in uml_package_results}
#     uml_classes = uml_model.ProjectClasses(
#         {
#             class_id: parse_uml_class(list(class_rows))
#             for class_id, class_rows in groupby(uml_class_results, itemgetter("class_id"))
#         }
#     )
#     uml_relations = uml_model.ProjectRelations(
#         {rel_row["id"]: parse_uml_relation(rel_row) for rel_row in uml_relation_results}
#     )

#     uml_project = uml_model.Project(
#         classes=uml_classes, packages=uml_packages, relations=uml_relations
#     )

#     schema = gen_schema(11, uml_project)
#     with open("out.yml", "w") as f:
#         yaml.dump(schema, f, indent=4, default_flow_style=False)


def frozenset_representer(dumper, data):
    assert type(data) == frozenset
    if len(data) == 0:
        return dumper.represent_set(data)

    for el in data:  # Only check first element.
        if type(el) == tuple and len(el) == 2:
            return dumper.represent_dict(dict(data))
        else:
            return dumper.represent_set(data)


def linkml_namedtuple_representer(dumper, data):
    return dumper.represent_dict(data._asdict())


def init_yaml_serializer():
    yaml.add_representer(frozenset, frozenset_representer)
    yaml.add_representer(linkml_model.Slot, linkml_namedtuple_representer)
    yaml.add_representer(linkml_model.Class, linkml_namedtuple_representer)
    yaml.add_representer(linkml_model.Enum, linkml_namedtuple_representer)
    yaml.add_representer(linkml_model.Schema, linkml_namedtuple_representer)
    yaml.add_representer(linkml_model.PermissibleValue, linkml_namedtuple_representer)


def main():
    init_yaml_serializer()

    for pkg_id in uml_project.packages:
        pkg_id = 11
        schema = gen_schema(pkg_id)
        with open(f"schemas/{pkg_id}.yml", "w") as f:
            yaml.dump(schema, f, indent=4, default_flow_style=False)
        # slot = linkml_model.Slot(name="JeMoeder", range="jeVader")
        # class_ = linkml_model.Class(name="God", attributes=frozenset({("JeMoeder", slot)}))
        # d = yaml.dump(class_, indent=4, default_flow_style=False)
        # pprint(d)
        break


if __name__ == "__main__":
    cProfile.run("main()", sort="cumtime")
    # main()
