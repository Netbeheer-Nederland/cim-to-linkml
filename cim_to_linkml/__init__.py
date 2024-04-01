from pprint import pprint
import sqlite3

from cim_to_linkml.read import read_uml_classes, read_uml_relations, read_uml_packages
from cim_to_linkml.parser import parse_uml_package


if __name__ == "__main__":
    db_file = "data/iec61970cim17v40_iec61968cim13v13b_iec62325cim03v17b_CIM100.1.1.1.qea"

    with sqlite3.connect(db_file) as conn:
        uml_class_rows = read_uml_classes(conn, include_attrs=True)
        uml_relation_rows = read_uml_relations(conn)
        uml_package_rows = read_uml_packages(conn)
    
    uml_packages = {id: parse_uml_package(id, uml_package_rows) for id in uml_package_rows}

    pprint(uml_packages)