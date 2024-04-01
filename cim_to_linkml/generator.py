from linkml_runtime import linkml_model
from linkml_runtime.utils.metamodelcore import Curie

import cim_to_linkml.uml_model as uml_model


CIM_PREFIX = "cim"


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
            "Duration": "int",
        }[val]
    except KeyError:
        raise TypeError(f"Data type `{val}` is not a CIM Primitive.")


def gen_safe_name(name: str) -> str:  # TODO: Implement and move.
    # Cleanup colons and weird characters.
    return name


def convert_camel_to_snake(name: str) -> str:  # TODO: Implement and move.
    return name


def gen_curie(name: str, prefix: str) -> Curie:  # TODO: Implement and move.
    # Also escape characters.
    return Curie(name)


def gen_schema(
    uml_classes: list[uml_model.Class],
    uml_relations: list[uml_model.Relation],
    uml_packages: list[uml_model.Package],
    uml_package_name: uml_model.PackageName,
) -> linkml_model.SchemaDefinition:
    schema = linkml_model.SchemaDefinition(
        id=gen_curie(uml_package_name, "cim"), name=uml_package_name
    )

    for uml_class in uml_classes:
        match uml_class.stereotype:
            case uml_model.ClassStereotype.PRIMITIVE:
                continue
            case uml_model.ClassStereotype.ENUMERATION:
                enum = gen_enum(uml_class)
                schema.enums[gen_safe_name(enum.name)] = enum
            # case uml_model.ClassStereotype.CIMDATATYPE:
            #     ... # TODO
            case None | _:
                class_ = gen_class(uml_class, uml_relations)
                schema.classes[gen_safe_name(class_.name)] = class_

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
            uml_relation.type == uml_model.RelationType.GENERALIZATION
            and uml_relation.source_class.id == uml_class.id
        ):
            super_class = uml_relation.dest_class
            return super_class


def gen_slot_from_attr(
    uml_attr: uml_model.Attribute, uml_class: uml_model.Class
) -> linkml_model.SlotDefinition:
    return linkml_model.SlotDefinition(
        name=convert_camel_to_snake(gen_safe_name(uml_attr.name)),
        range=(
            map_primitive_data_type(uml_attr.type)
            if uml_attr.type.stereotype == uml_model.ClassStereotype.PRIMITIVE
            else convert_camel_to_snake(gen_safe_name(uml_attr.type.name))
        ),
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
    uml_relation: uml_model.Relation, uml_class: uml_model.Class
) -> linkml_model.SlotDefinition:
    return linkml_model.SlotDefinition(
        name=convert_camel_to_snake(
            gen_safe_name(uml_relation.dest_role or uml_relation.dest_class.name)
        ),
        range=convert_camel_to_snake(gen_safe_name(uml_relation.dest_class.name)),
        description=uml_relation.source_role_note,  # TODO: Is this the right one?
        required=_slot_required(uml_relation.source_card.lower_bound),
        multivalued=_slot_multivalued(uml_relation.source_card.upper_bound),
        slot_uri=gen_curie(
            f"{uml_class.name}.{uml_relation.source_role or uml_relation.source_class.name}",
            CIM_PREFIX,
        ),
    )


def gen_class(
    uml_class: uml_model.Class, uml_relations: list[uml_model.Relation]
) -> linkml_model.ClassDefinition:
    super_class = get_super_class(uml_class, uml_relations)

    attr_slots = {
        convert_camel_to_snake(gen_safe_name(attr.name)): gen_slot_from_attr(attr, uml_class)
        for attr in uml_class.attributes.values()
    }
    relation_slots = {
        convert_camel_to_snake(
            gen_safe_name(rel.dest_role or rel.dest_class.name)
        ): gen_slot_from_relation(rel, uml_class)
        for rel in uml_relations
        if rel.source_class.id == uml_class.id
        if rel.type != uml_model.RelationType.GENERALIZATION
    }

    return linkml_model.ClassDefinition(
        name=gen_safe_name(uml_class.name),
        class_uri=gen_curie(uml_class.name, CIM_PREFIX),
        is_a=super_class.name if super_class else None,
        description=uml_class.note,
        attributes=attr_slots | relation_slots,
    )
