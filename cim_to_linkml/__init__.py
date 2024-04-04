import os
import yaml
from itertools import groupby
from operator import itemgetter
import sqlite3
import cProfile

import cim_to_linkml.uml_model as uml_model
import cim_to_linkml.linkml_model as linkml_model

from cim_to_linkml.read import read_uml_classes, read_uml_relations, read_uml_packages
from cim_to_linkml.parser import parse_uml_package, parse_uml_class, parse_uml_relation
from cim_to_linkml.generator import LinkMLGenerator
import cim_to_linkml.serializer as serializer


def init_yaml_serializer():
    yaml.add_representer(type(None), serializer.represent_none)
    yaml.add_representer(frozenset, serializer.frozenset_representer)
    yaml.add_representer(linkml_model.Slot, serializer.linkml_namedtuple_representer)
    yaml.add_representer(linkml_model.Class, serializer.linkml_namedtuple_representer)
    yaml.add_representer(linkml_model.Enum, serializer.linkml_namedtuple_representer)
    yaml.add_representer(linkml_model.Schema, serializer.linkml_namedtuple_representer)
    yaml.add_representer(linkml_model.PermissibleValue, serializer.linkml_namedtuple_representer)


def main():
    init_yaml_serializer()
    db_file = "data/iec61970cim17v40_iec61968cim13v13b_iec62325cim03v17b_CIM100.1.1.1.qea"

    with sqlite3.connect(db_file) as conn:
        uml_class_results = read_uml_classes(conn)
        uml_relation_results = read_uml_relations(conn)
        uml_package_results = read_uml_packages(conn)

    uml_packages = uml_model.Packages({parse_uml_package(pkg_row) for pkg_row in uml_package_results})
    uml_classes = uml_model.Classes(
        {parse_uml_class(list(class_rows)) for _, class_rows in groupby(uml_class_results, itemgetter("class_id"))}
    )
    uml_relations = uml_model.Relations({parse_uml_relation(rel_row) for rel_row in uml_relation_results})

    uml_project = uml_model.Project(classes=uml_classes, packages=uml_packages, relations=uml_relations)

    generator = LinkMLGenerator(uml_project)
    for pkg_id in uml_project.packages.by_id:
        pkg_id = 11

        # TODO: This logic could probably be moved to the generator class.
        pkg_path_parts = generator._build_package_path(pkg_id)[::-1]

        if not pkg_path_parts:
            continue

        pkg_dir_path = os.path.join("schemas", os.sep.join(pkg_path_parts[:-1]))
        pkg_filename = pkg_path_parts[-1] + ".yml"
        os.makedirs(pkg_dir_path, exist_ok=True)

        schema = generator.gen_schema(pkg_id)
        with open(os.path.join(pkg_dir_path, pkg_filename), "w") as f:
            yaml.dump(schema, f, indent=4, default_flow_style=False, sort_keys=False)
        break


if __name__ == "__main__":
    # cProfile.run("main()", sort="tottime")
    main()
