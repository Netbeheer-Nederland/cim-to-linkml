import sqlite3
from itertools import groupby
from operator import itemgetter

from cim_to_linkml.cim18.uml.class_.parse import parse_uml_class
from cim_to_linkml.cim18.uml.package.parse import parse_uml_package
from cim_to_linkml.cim18.uml.project.model import Project, Relations, Classes, Packages
from cim_to_linkml.cim18.uml.relation.parse import parse_uml_relation


def parse_uml_relations(relations: sqlite3.Cursor) -> Relations:
    return Relations({relation_row["id"]: parse_uml_relation(relation_row) for relation_row in relations})


def parse_uml_classes(classes: sqlite3.Cursor) -> Classes:
    return Classes({class_id: parse_uml_class(class_rows) for class_id, class_rows in groupby(classes, itemgetter("class_id"))})


def parse_uml_packages(packages: sqlite3.Cursor) -> Packages:
    packages = list(packages)  # Materialize for reuse for recursively checking for package statuses.

    return Packages({package_row["id"]: parse_uml_package(package_row, packages) for package_row in packages})


def parse_uml_project(
        packages: sqlite3.Cursor,
        classes: sqlite3.Cursor,
        relations: sqlite3.Cursor,
) -> Project:
    return Project(
        packages=parse_uml_packages(packages),
        classes=parse_uml_classes(classes),
        relations=parse_uml_relations(relations),
    )
