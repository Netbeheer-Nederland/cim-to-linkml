from pprint import pprint
import sqlite3

from cim_to_linkml.read import read_uml_classes, read_uml_relations, read_uml_packages
from cim_to_linkml.parser import parse_uml_package, parse_uml_class


if __name__ == "__main__":
    db_file = "data/iec61970cim17v40_iec61968cim13v13b_iec62325cim03v17b_CIM100.1.1.1.qea"

    with sqlite3.connect(db_file) as conn:
        uml_class_results = read_uml_classes(conn)
        uml_relation_results = read_uml_relations(conn)
        uml_package_results = read_uml_packages(conn)

    pprint(uml_class_results)
    # uml_packages = {id: parse_uml_package(id, uml_package_rows) for id in uml_package_rows}
    # pprint(uml_class_results)
    # uml_classes = {id: parse_uml_class(id, uml_class_results) for id in uml_class_results}

    # pprint(uml_classes)
