import sqlite3
from itertools import groupby
from operator import itemgetter
from datetime import datetime
from pprint import pprint


import cim_to_linkml.uml_model as uml_model


def parse_cardinality_tuple(val: str | None) -> uml_model.Cardinality:
    if val is None:
        return uml_model.Cardinality()

    lb, _, ub = val.partition("..")

    lb.replace("n", "*")
    ub.replace("n", "*")

    return uml_model.Cardinality(lower_bound=lb, upper_bound=ub)


def parse_cardinality_val(val: str | None) -> uml_model.CardinalityValue | None:
    match val:
        case None:
            return None
        case "*":
            return "*"
        case _:
            return int(val)


def parse_iso_datetime_val(val: str | None) -> datetime:
    if val is None:
        return datetime.now()

    return datetime.fromisoformat(val)


def parse_uml_package(package_row: sqlite3.Cursor) -> uml_model.Package:
    uml_package: dict = dict(package_row)
    return uml_model.Package(
        id=uml_package["id"],
        name=uml_package["name"],
        author=uml_package["author"],
        parent=uml_package["parent_id"],
        created_date=parse_iso_datetime_val(uml_package["created_date"]),
        modified_date=parse_iso_datetime_val(uml_package["modified_date"]),
        notes=uml_package["note"],
    )


def parse_uml_relation(relation_row: sqlite3.Cursor) -> uml_model.Relation:
    uml_relation: dict = dict(relation_row)
    pprint(uml_relation)

    try:
        direction = uml_model.RelationDirection(uml_relation["direction"])
    except ValueError:
        direction = None

    return uml_model.Relation(
        id=uml_relation["id"],
        connector_type=uml_model.RelationType(uml_relation["type"]),
        source_class=uml_relation["start_object_id"],
        dest_class=uml_relation["end_object_id"],
        direction=direction,
        source_card=parse_cardinality_tuple(uml_relation["source_card"]),
        source_role=uml_relation["source_role"],
        source_role_note=uml_relation["source_role_note"],
        dest_card=parse_cardinality_tuple(uml_relation["dest_card"]),
        dest_role=uml_relation["dest_role"],
        dest_role_note=uml_relation["dest_role_note"],
    )


def parse_uml_class_attr(attr: dict) -> uml_model.Attribute:
    try:
        stereotype = uml_model.AttributeStereotype(attr["attr_stereotype"])
    except ValueError:
        stereotype = None

    return uml_model.Attribute(
        id=attr["attr_id"],
        name=attr["attr_name"],
        lower_bound=parse_cardinality_val(attr["attr_lower_bound"]),
        upper_bound=parse_cardinality_val(attr["attr_upper_bound"]),
        type=attr["attr_type"],
        default=attr["attr_default"],
        notes=attr["attr_notes"],
        stereotype=stereotype,
    )


def parse_uml_class(class_rows: list[sqlite3.Cursor]) -> uml_model.Class:
    try:
        stereotype = uml_model.ClassStereotype(class_rows[0]["class_stereotype"])
    except ValueError:
        stereotype = None

    return uml_model.Class(
        id=class_rows[0]["class_id"],
        name=class_rows[0]["class_name"],
        author=class_rows[0]["class_author"],
        package=class_rows[0]["class_package_id"],
        attributes={
            attr_name: parse_uml_class_attr(next(attr))
            for attr_name, attr in groupby(class_rows, itemgetter("attr_name"))
        },
        created_date=parse_iso_datetime_val(class_rows[0]["class_created_date"]),
        modified_date=parse_iso_datetime_val(class_rows[0]["class_modified_date"]),
        note=class_rows[0]["class_note"],
        stereotype=stereotype,
    )
