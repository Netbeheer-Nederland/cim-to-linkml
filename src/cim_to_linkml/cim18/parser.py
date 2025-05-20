import sqlite3
from datetime import datetime
from itertools import groupby
from operator import itemgetter
from typing import Iterator

import cim_to_linkml.cim18.uml_model as uml_model


def parse_cardinality(val: str | None) -> uml_model.Cardinality:
    if val is None:
        return uml_model.Cardinality()

    lb, _, ub = val.partition("..")

    return uml_model.Cardinality(
        lower_bound=parse_cardinality_val(lb),
        upper_bound=parse_cardinality_val(ub),
    )


def parse_cardinality_val(val: str | None) -> uml_model.CardinalityValue:
    match val:
        case "" | None:
            return 0
        case "n" | "*":
            return "*"
        case _:
            return int(val)


def parse_iso_datetime_val(val: str | None) -> datetime:
    if val is None:
        return datetime.now()

    return datetime.fromisoformat(val)


def parse_uml_relation(relation_row: sqlite3.Cursor) -> uml_model.Relation:
    uml_relation = dict(relation_row)

    try:
        direction = uml_model.RelationDirection(uml_relation["direction"])
    except ValueError:
        direction = None

    return uml_model.Relation(
        id=uml_relation["id"],
        type=uml_model.RelationType(uml_relation["type"]),
        source_class=uml_relation["start_object_id"],
        dest_class=uml_relation["end_object_id"],
        direction=direction,
        source_card=parse_cardinality(uml_relation["source_card"]),
        source_role=uml_relation["source_role"],
        source_role_note=uml_relation["source_role_note"],
        dest_card=parse_cardinality(uml_relation["dest_card"]),
        dest_role=uml_relation["dest_role"],
        dest_role_note=uml_relation["dest_role_note"],
    )


def parse_uml_class_attribute(attr: dict) -> uml_model.Attribute:
    try:
        stereotype = uml_model.AttributeStereotype(attr["attr_stereotype"])
    except ValueError:
        stereotype = None

    return uml_model.Attribute(
        id=attr["attr_id"],
        class_=attr["class_id"],
        name=attr["attr_name"],
        lower_bound=parse_cardinality_val(attr["attr_lower_bound"]),
        upper_bound=parse_cardinality_val(attr["attr_upper_bound"]),
        type=attr["attr_type"],
        default=attr["attr_default"],
        notes=attr["attr_notes"],
        stereotype=stereotype,
    )


def parse_uml_attributes(rows: list[dict]) -> dict[uml_model.AttributeID, uml_model.Attribute]:
    return {attr_id: parse_uml_class_attribute(attr)
                for _, attr_ in groupby(rows, itemgetter("attr_name"))
                if (attr := next(attr_))
                if attr["attr_id"] is not None
                if (attr_id := int(attr["attr_id"]))}


# TODO: Improve type signature. `Iterator` says too little.
def parse_uml_class(class_rows: Iterator) -> uml_model.Class:
    class_rows = [dict(row) for row in class_rows]  # Materialize.

    try:
        stereotype = uml_model.ClassStereotype(class_rows[0]["class_stereotype"])
    except ValueError:
        stereotype = None

    return uml_model.Class(
        id=int(class_rows[0]["class_id"]),
        name=class_rows[0]["class_name"],
        author=class_rows[0]["class_author"],
        package=int(class_rows[0]["class_package_id"]),
        attributes=parse_uml_attributes(class_rows),
        created_date=parse_iso_datetime_val(class_rows[0]["class_created_date"]),
        modified_date=parse_iso_datetime_val(class_rows[0]["class_modified_date"]),
        note=class_rows[0]["class_note"],
        stereotype=stereotype,
    )


def is_informal_package(package: sqlite3.Row, packages: list[sqlite3.Row]) -> bool:
    if package["id"] in uml_model.INFORMAL_PACKAGES:
        return True

    try:
        parent_package = [p for p in packages if p["id"] == package["parent_id"]][0]
    except IndexError:
        return False

    return False or is_informal_package(parent_package, packages)


def is_documentation_package(package: sqlite3.Row, packages: list[sqlite3.Row]) -> bool:
    if package["id"] in uml_model.DOCUMENTATION_PACKAGES:
        return True

    try:
        parent_package = [p for p in packages if p["id"] == package["parent_id"]][0]
    except IndexError:
        return False

    return False or is_documentation_package(parent_package, packages)


def parse_uml_package(package: sqlite3.Row, packages: list[sqlite3.Row]) -> uml_model.Package:
    return uml_model.Package(
        id=package["id"],
        name=package["name"],
        notes=package["note"],
        author=package["author"],
        created_date=parse_iso_datetime_val(package["created_date"]),
        modified_date=parse_iso_datetime_val(package["modified_date"]),
        parent=package["parent_id"],
        is_informal=is_informal_package(package, packages),
        is_documentation=is_documentation_package(package, packages),
    )


def parse_uml_relations(relations: sqlite3.Cursor) -> dict[uml_model.ObjectID, uml_model.Relation]:
    return {relation_row["id"]: parse_uml_relation(relation_row) for relation_row in relations}


def parse_uml_classes(classes: sqlite3.Cursor) -> dict[uml_model.ObjectID, uml_model.Class]:
    return {class_id: parse_uml_class(class_rows) for class_id, class_rows in groupby(classes, itemgetter("class_id"))}


def parse_uml_packages(packages: sqlite3.Cursor) -> dict[uml_model.ObjectID, uml_model.Package]:
    packages = list(packages)  # Materialize for reuse for recursively checking for informal and documentation packages.

    return {package_row["id"]: parse_uml_package(package_row, packages) for package_row in packages}


def parse_uml_project(
    packages: sqlite3.Cursor,
    classes: sqlite3.Cursor,
    relations: sqlite3.Cursor,
) -> uml_model.Project:
    return uml_model.Project(
        packages=parse_uml_packages(packages),
        classes=parse_uml_classes(classes),
        relations=parse_uml_relations(relations),
    )
