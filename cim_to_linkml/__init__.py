import cProfile
import os
import sqlite3
from pprint import pprint

import yaml

from cim_to_linkml.generator import LinkMLGenerator
from cim_to_linkml.parser import parse_uml_project
from cim_to_linkml.read import read_uml_classes, read_uml_project
from cim_to_linkml.writer import init_yaml_serializer, write_schema

init_yaml_serializer()


def main():
    db_file = "data/iec61970cim17v40_iec61968cim13v13b_iec62325cim03v17b_CIM100.1.1.1.qea"
    with sqlite3.connect(db_file) as conn:
        uml_project = parse_uml_project(*read_uml_project(conn))

    generator = LinkMLGenerator(uml_project)
    for pkg_id in generator.uml_project.packages.by_id:
        if pkg_id == 2:
            continue  # `Model` base package.

        if pkg_id != 11:
            continue

        schema = generator.gen_schema_for_package(pkg_id)
        write_schema(schema)


if __name__ == "__main__":
    # cProfile.run("main()", sort="tottime")
    main()
