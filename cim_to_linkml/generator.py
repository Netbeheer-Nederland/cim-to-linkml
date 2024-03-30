from typing import Iterable

from linkml_runtime import linkml_model
from linkml_runtime.utils.metamodelcore import Curie, empty_list

import cim_to_linkml.uml_model as uml_model


CIM_PREFIX = "cim"


def gen_safe_name(name: str) -> str:  # TODO: Implement and move.
    # Cleanup colons and weird characters.
    return name


def convert_camel_to_snake(name: str) -> str:  # TODO: Implement and move.
    return name


def gen_curie(name: str, prefix: str) -> Curie:  # TODO: Implement and move.
    # Also escape characters.
    return Curie(name)


def gen_schema(
    uml_classes: Iterable[uml_model.Class],
    uml_relations: Iterable[uml_model.Relation],
    uml_packages: Iterable[uml_model.Package],
    uml_package_name: uml_model.PackageName,
) -> linkml_model.SchemaDefinition:
    schema = linkml_model.SchemaDefinition(
        id=gen_curie(uml_package_name, "cim"),
        name=uml_package_name,
    )

    # Initialize `enums` and `classes` dicts to fix typing issues.
    schema.enums = {}  
    schema.classes = {}

    for uml_class in uml_classes:
        match uml_class.stereotype:
            case uml_model.ClassStereotype.ENUMERATION:
                enum = gen_enum(uml_class)
                schema.enums[enum.name] = enum

    return schema


def gen_enum(uml_enum: uml_model.Class) -> linkml_model.EnumDefinition:
    assert uml_enum.stereotype == uml_model.ClassStereotype.ENUMERATION

    return linkml_model.EnumDefinition(
        name=gen_safe_name(uml_enum.name),
        enum_uri=gen_curie(uml_enum.name, CIM_PREFIX),
        description=uml_enum.note,
        permissible_values={
            uml_enum_val.name: linkml_model.PermissibleValue(
                text=convert_camel_to_snake(gen_safe_name(uml_enum_val.name)),
                meaning=gen_curie(f"{uml_enum}.{uml_enum_val.name}", CIM_PREFIX),
            )
            for uml_enum_val in uml_enum.attributes.values()
        },
    )


def get_super_class(
    uml_class: uml_model.Class, uml_relations: list[uml_model.Relation]
) -> uml_model.Class | None:
    for uml_relation in uml_relations:
        if (
            uml_relation.connector_type == uml_model.RelationType.GENERALIZATION
            and uml_relation.source_class.id == uml_class.id
        ):
            super_class = uml_relation.dest_class
            return super_class


def gen_class(
    uml_class: uml_model.Class, uml_relations: list[uml_model.Relation]
) -> linkml_model.ClassDefinition:
    super_class = get_super_class(uml_class, uml_relations)

    return linkml_model.ClassDefinition(
        name=gen_safe_name(uml_class.name),
        class_uri=gen_curie(uml_class.name, CIM_PREFIX),
        is_a=super_class.name if super_class else None,
        description=uml_class.note,
        attributes={},  # TODO
    )
