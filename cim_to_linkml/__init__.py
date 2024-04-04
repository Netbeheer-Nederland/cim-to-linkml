import cProfile
import os
import sqlite3

import yaml

from cim_to_linkml.generator import LinkMLGenerator
from cim_to_linkml.parser import parse_project
from cim_to_linkml.read import read_project
from cim_to_linkml.writer import init_yaml_serializer

init_yaml_serializer()


def main():
    db_file = "data/iec61970cim17v40_iec61968cim13v13b_iec62325cim03v17b_CIM100.1.1.1.qea"
    with sqlite3.connect(db_file) as conn:
        uml_project = parse_project(*read_project(conn))
                                
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
