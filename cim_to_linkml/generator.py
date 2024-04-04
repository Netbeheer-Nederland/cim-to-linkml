from pprint import pprint
from itertools import groupby, chain
from functools import lru_cache
from operator import attrgetter, itemgetter, add
from urllib.parse import quote
from typing import Optional

import cim_to_linkml.uml_model as uml_model
import cim_to_linkml.linkml_model as linkml_model


CIM_PREFIX = "cim"


### TEST
# import sqlite3
# import yaml
# from cim_to_linkml.read import read_uml_classes, read_uml_packages, read_uml_relations
# from cim_to_linkml.parser import parse_uml_package, parse_uml_class, parse_uml_relation


# db_file = "data/iec61970cim17v40_iec61968cim13v13b_iec62325cim03v17b_CIM100.1.1.1.qea"

# with sqlite3.connect(db_file) as conn:
#     uml_class_results = read_uml_classes(conn)
#     uml_relation_results = read_uml_relations(conn)
#     uml_package_results = read_uml_packages(conn)

# uml_packages = {pkg_row["id"]: parse_uml_package(pkg_row) for pkg_row in uml_package_results}
# uml_classes = uml_model.Classes(
#     {
#         class_id: parse_uml_class(list(class_rows))
#         for class_id, class_rows in groupby(uml_class_results, itemgetter("class_id"))
#     }
# )
# uml_relations = uml_model.Relations(
#     {rel_row["id"]: parse_uml_relation(rel_row) for rel_row in uml_relation_results}
# )

# uml_project = uml_model.Project(classes=uml_classes, packages=uml_packages, relations=uml_relations)


def map_primitive_data_type(val):
    try:
        return {
            "Float": "float",
            "Integer": "integer",
            "DateTime": "date",
            "String": "string",
            "Boolean": "boolean",
            "Decimal": "double",  # Is this right?
            "MonthDay": "date",  # Is this right?
            "Date": "date",
            "Time": "time",
            "Duration": "integer",
        }[val]
    except KeyError:
        raise TypeError(f"Data type `{val}` is not a CIM Primitive.")


def gen_safe_name(name: str) -> str:  # TODO: Implement and move.
    # Cleanup colons and weird characters.
    return name


def convert_camel_to_snake(name: str) -> str:  # TODO: Implement and move.
    return name


def gen_curie(name: str, prefix: str) -> str:  # TODO: Implement and move.
    # Also escape characters.
    return f"{prefix}:{quote(name)}"


# @lru_cache(maxsize=2048)
def _gen_elements(
    uml_class: uml_model.Class,
    uml_project: uml_model.Project,
    results: Optional[
        tuple[
            frozenset[tuple[uml_model.ObjectID, linkml_model.Class]],
            frozenset[tuple[str, linkml_model.Enum]],
            frozenset[uml_model.ObjectID],
        ]
    ] = None,
) -> tuple[
    frozenset[tuple[str, linkml_model.Class]],
    frozenset[tuple[str, linkml_model.Enum]],
    frozenset[uml_model.ObjectID],
]:
    if results is None:
        results = frozenset(), frozenset(), frozenset()

    match uml_class.stereotype:
        case uml_model.ClassStereotype.PRIMITIVE:
            return results
        case uml_model.ClassStereotype.ENUMERATION:
            enum = gen_enum(uml_class, uml_project)
            results = results[0], results[1] | {(enum.name, enum)}, results[2] | {uml_class.id}
        case uml_model.ClassStereotype.CIMDATATYPE | None | _:
            class_ = gen_class(uml_class, uml_project)
            results = results[0] | {(class_.name, class_)}, results[1], results[2] | {uml_class.id}

    uml_dep_classes = set()

    uml_super_class = get_super_class(uml_class, uml_project)
    if uml_super_class:
        uml_dep_classes.add(uml_super_class)

    uml_dep_classes |= get_attr_type_classes(uml_class, uml_project) | get_rel_type_classes(
        uml_class, uml_project
    )

    for uml_dep_class in uml_dep_classes:
        if uml_dep_class.id in results[2]:
            continue
        c, e, p = _gen_elements(uml_dep_class, uml_project, results)
        results = results[0] | c, results[1] | e, results[2] | p
    return results


def gen_schema(
    uml_package_id: uml_model.ObjectID, uml_project: uml_model.Project
) -> linkml_model.Schema:
    uml_package = uml_project.packages.by_id[uml_package_id]

    classes = frozenset()
    enums = frozenset()
    processed_ids = frozenset()
    # for uml_class in uml_project.classes.by_id.values():
    for uml_class in uml_project.classes.by_pkg_id.get(uml_package_id, []):
        print(uml_class.name)
        new_classes, new_enums, new_processed_ids = _gen_elements(
            uml_class,
            uml_project,
            (classes, enums, processed_ids),
        )

        classes = classes | new_classes
        enums = enums | new_enums
        processed_ids = processed_ids | new_processed_ids

    schema = linkml_model.Schema(
        id=gen_curie(uml_package.name, "cim"),
        name=uml_package.name,
        enums=enums,
        classes=classes,
    )

    return schema


@lru_cache(maxsize=2048)
def gen_enum(uml_enum: uml_model.Class, uml_project: uml_model.Project) -> linkml_model.Enum:
    assert uml_enum.stereotype == uml_model.ClassStereotype.ENUMERATION
    enum_name = gen_safe_name(uml_enum.name)

    return linkml_model.Enum(
        name=gen_safe_name(enum_name),
        enum_uri=gen_curie(uml_enum.name, CIM_PREFIX),
        description=uml_enum.note,
        permissible_values=frozenset(
            {
                (
                    uml_enum_val.name,
                    linkml_model.PermissibleValue(
                        text=enum_val, meaning=gen_curie(f"{enum_name}.{enum_val}", CIM_PREFIX)
                    ),
                )
                for uml_enum_val in uml_enum.attributes
                if (enum_val := convert_camel_to_snake(gen_safe_name(uml_enum_val.name)))
            }
        ),
    )


@lru_cache(maxsize=2048)
def get_super_class(
    uml_class: uml_model.Class, uml_project: uml_model.Project
) -> Optional[uml_model.Class]:
    rels = uml_project.relations.by_source_id.get(uml_class.id, [])
    for uml_relation in rels:
        try:
            source_class = uml_project.classes.by_id[uml_relation.source_class]
        except KeyError as e:
            continue  # Bad data, but no superclass for sure.
        if (
            uml_relation.type == uml_model.RelationType.GENERALIZATION
            and source_class.id == uml_class.id
        ):
            super_class = uml_project.classes.by_id[uml_relation.dest_class]
            return super_class
    return None


@lru_cache(maxsize=2048)
def get_attr_type_classes(
    uml_class: uml_model.Class, uml_project: uml_model.Project
) -> frozenset[uml_model.Class]:
    type_classes = {
        class_
        for attr in uml_class.attributes
        if attr.type is not None
        if (class_ := uml_project.classes.by_name[attr.type])
    }

    return frozenset(type_classes)


@lru_cache(maxsize=2048)
def get_rel_type_classes(
    uml_class: uml_model.Class, uml_project: uml_model.Project
) -> frozenset[uml_model.Class]:
    from_classes = set()
    to_classes = set()

    for rel in uml_project.relations.by_id.values():
        if rel.type == uml_model.RelationType.GENERALIZATION:
            continue
        match uml_class.id:
            case rel.source_class:
                dest_class = uml_project.classes.by_id[rel.dest_class]
                to_classes.add(dest_class)
            case rel.dest_class:
                source_class = uml_project.classes.by_id[rel.source_class]
                from_classes.add(source_class)

    return frozenset(from_classes | to_classes)


def gen_slot_from_attr(
    uml_attr: uml_model.Attribute, uml_class: uml_model.Class, uml_project: uml_model.Project
) -> linkml_model.Slot:
    # range_ = None
    # if uml_attr.type is not None:
    type_class = uml_project.classes.by_name[uml_attr.type]
    if type_class.stereotype == uml_model.ClassStereotype.PRIMITIVE:
        range_ = map_primitive_data_type(uml_attr.type)
    else:
        range_ = convert_camel_to_snake(gen_safe_name(type_class.name))

    return linkml_model.Slot(
        name=convert_camel_to_snake(gen_safe_name(uml_attr.name)),
        range=range_,
        description=uml_attr.notes,
        required=_slot_required(uml_attr.lower_bound),
        multivalued=_slot_multivalued(uml_attr.lower_bound),
        slot_uri=gen_curie(f"{uml_class.name}.{uml_attr.name}", CIM_PREFIX),
    )


def _slot_required(lower_bound: uml_model.CardinalityValue) -> bool:
    return lower_bound == "*" or lower_bound > 0


def _slot_multivalued(upper_bound: uml_model.CardinalityValue) -> bool:
    return upper_bound == "*" or upper_bound > 1


def gen_slot_from_relation(
    uml_relation: uml_model.Relation, uml_project: uml_model.Project, direction
) -> linkml_model.Slot:
    source_class = uml_project.classes.by_id[uml_relation.source_class]
    dest_class = uml_project.classes.by_id[uml_relation.dest_class]

    match direction:
        case "source->dest":
            return linkml_model.Slot(
                name=convert_camel_to_snake(
                    gen_safe_name(uml_relation.dest_role or dest_class.name)
                ),
                range=gen_safe_name(dest_class.name),
                description=uml_relation.dest_role_note,
                required=_slot_required(uml_relation.dest_card.lower_bound),
                multivalued=_slot_multivalued(uml_relation.dest_card.upper_bound),
                slot_uri=gen_curie(
                    f"{source_class.name}.{uml_relation.dest_role or dest_class.name}",
                    CIM_PREFIX,
                ),
            )
        case "dest->source":
            return linkml_model.Slot(
                name=convert_camel_to_snake(
                    gen_safe_name(uml_relation.source_role or source_class.name)
                ),
                range=gen_safe_name(source_class.name),
                description=uml_relation.source_role_note,
                required=_slot_required(uml_relation.source_card.lower_bound),
                multivalued=_slot_multivalued(uml_relation.source_card.upper_bound),
                slot_uri=gen_curie(
                    f"{dest_class.name}.{uml_relation.source_role or source_class.name}",
                    CIM_PREFIX,
                ),
            )
        case _:
            raise TypeError(
                f"Provided direction value was invalid. (relation ID: {uml_relation.id})"
            )


@lru_cache(maxsize=2048)
def gen_class(uml_class: uml_model.Class, uml_project: uml_model.Project) -> linkml_model.Class:
    super_class = get_super_class(uml_class, uml_project)

    attr_slots = {
        (slot.name, slot)
        for uml_attr in uml_class.attributes
        if (slot := gen_slot_from_attr(uml_attr, uml_class, uml_project))
    }

    from_relation_slots = {
        (slot.name, slot)
        for rel in uml_project.relations.by_source_id.get(uml_class.id, [])
        if rel and rel.type != uml_model.RelationType.GENERALIZATION
        if (slot := gen_slot_from_relation(rel, uml_project, "source->dest"))
    }

    to_relation_slots = {
        (slot.name, slot)
        for rel in uml_project.relations.by_dest_id.get(uml_class.id, [])
        if rel and rel.type != uml_model.RelationType.GENERALIZATION
        if (slot := gen_slot_from_relation(rel, uml_project, "dest->source"))
    }

    class_ = linkml_model.Class(
        name=gen_safe_name(uml_class.name),
        class_uri=gen_curie(uml_class.name, CIM_PREFIX),
        is_a=super_class.name if super_class else None,
        description=uml_class.note,
        attributes=frozenset(attr_slots | from_relation_slots | to_relation_slots),
    )

    return class_
