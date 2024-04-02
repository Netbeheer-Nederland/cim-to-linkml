from pprint import pprint
from itertools import groupby, chain
from operator import attrgetter, itemgetter, add
from urllib.parse import quote

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
    # return Curie(name)
    return f"{prefix}:{quote(name)}"


def _get_package_hierarchy(
    pkg_id: uml_model.ObjectID, pkgs: dict[uml_model.ObjectID, uml_model.Package]
) -> list[uml_model.Package]:
    pkg = pkgs[pkg_id]

    if pkg.parent in [None, 0]:  # Package `0` does not exist; treat it as top-level.
        return []

    return [pkgs[pkg.parent].id] + _get_package_hierarchy(pkg.parent, pkgs)


def _gen_class_deps(
    uml_class: uml_model.Class, uml_project: uml_model.Project
) -> tuple[list[linkml_model.ClassDefinition], list[linkml_model.EnumDefinition]]:
    # TODO: Extend with relations.
    classes = []
    enums = []

    uml_super_class = get_super_class(uml_class, uml_project)
    uml_attr_type_classes = get_attr_type_classes(uml_class, uml_project)

    if not (uml_super_class or uml_attr_type_classes):
        return classes, enums

    if uml_super_class:
        super_class = gen_class(uml_super_class, uml_project)
        classes.append(super_class)
        super_class_deps = _gen_class_deps(uml_super_class, uml_project)
    else:
        super_class_deps = ([], [])

    for uml_attr_type_class in uml_attr_type_classes.values():
        if uml_attr_type_class.stereotype == uml_model.ClassStereotype.ENUMERATION:
            attr_type_enum = gen_enum(uml_attr_type_class)
            enums.append(attr_type_enum)
        else:  # Class.
            attr_type_class = gen_class(uml_attr_type_class, uml_project)
            classes.append(attr_type_class)

    if len(uml_attr_type_classes) == 0:
        uml_attr_type_classes_deps = ([], [])
    elif len(uml_attr_type_classes) == 1:
        uml_attr_type_classes_deps = _gen_class_deps(
            list(uml_attr_type_classes.values())[0], uml_project
        )
    else:
        uml_attr_type_classes_deps = ([], [])
        for type_class in uml_attr_type_classes.values():
            deps = _gen_class_deps(type_class, uml_project)
            uml_attr_type_classes = (
                uml_attr_type_classes_deps[0] + deps[0],
                uml_attr_type_classes_deps[1] + deps[1],
            )

    return (
        classes + super_class_deps[0] + uml_attr_type_classes_deps[0],
        enums + super_class_deps[1] + uml_attr_type_classes_deps[1],
    )


def gen_schema(
    uml_package_id: uml_model.ObjectID, uml_project: uml_model.Project
) -> linkml_model.SchemaDefinition:
    uml_package = uml_project.packages[uml_package_id]
    schema = linkml_model.SchemaDefinition(
        id=gen_curie(uml_package.name, "cim"),
        name=uml_package.name,
    )
    # package_hierarchy = [
    #     uml_package_id,
    #     *_get_package_hierarchy(uml_package_id, uml_project.packages),
    # ]
    classes_by_package_id = {
        pkg_id: list(classes)
        for pkg_id, classes in groupby(
            sorted(uml_project.classes.values(), key=attrgetter("package")), attrgetter("package")
        )
    }

    for uml_class in classes_by_package_id[uml_package_id]:
        match uml_class.stereotype:
            case uml_model.ClassStereotype.PRIMITIVE:
                continue
            case uml_model.ClassStereotype.ENUMERATION:
                enum = gen_enum(uml_class)
                schema.enums[gen_safe_name(enum.name)] = enum
            # case uml_model.ClassStereotype.CIMDATATYPE:
            #     ... # TODO
            case None | _:
                class_ = gen_class(uml_class, uml_project)
                schema.classes[gen_safe_name(class_.name)] = class_

                dep_classes, dep_enums = _gen_class_deps(uml_class, uml_project)
                schema.classes.update({gen_safe_name(c.name): c for c in dep_classes})
                schema.enums.update({gen_safe_name(e.name): e for e in dep_enums})

    return schema


def gen_enum(uml_enum: uml_model.Class) -> linkml_model.EnumDefinition:
    assert uml_enum.stereotype == uml_model.ClassStereotype.ENUMERATION
    enum_name = gen_safe_name(uml_enum.name)

    return linkml_model.EnumDefinition(
        name=enum_name,
        enum_uri=gen_curie(uml_enum.name, CIM_PREFIX),
        description=uml_enum.note,
        permissible_values={
            convert_camel_to_snake(gen_safe_name(uml_enum_val.name)): linkml_model.PermissibleValue(
                text=enum_val,
                meaning=gen_curie(f"{enum_name}.{enum_val}", CIM_PREFIX),
            )
            for uml_enum_val in uml_enum.attributes.values()
            if (enum_val := convert_camel_to_snake(gen_safe_name(uml_enum_val.name)))
        },
    )


def get_super_class(
    uml_class: uml_model.Class, uml_project: uml_model.Project
) -> uml_model.Class | None:
    for uml_relation in uml_project.relations.values():
        try:
            source_class = uml_project.classes[uml_relation.source_class]
        except KeyError as e:
            continue  # Bad data, but no superclass for sure.
        if (
            uml_relation.type == uml_model.RelationType.GENERALIZATION
            and source_class.id == uml_class.id
        ):
            super_class = uml_project.classes[uml_relation.dest_class]
            return super_class
    return None


def get_super_classes(
    uml_class: uml_model.Class, uml_project: uml_model.Project
) -> list[uml_model.Class]:
    super_class = get_super_class(uml_class, uml_project)

    if super_class is None:
        return []

    return [super_class] + get_super_classes(super_class, uml_project)


def get_attr_type_classes(
    uml_class: uml_model.Class, uml_project: uml_model.Project
) -> dict[uml_model.ObjectID, uml_model.Class]:
    classes_by_name = {
        name: next(classes)
        for name, classes in groupby(
            sorted(uml_project.classes.values(), key=attrgetter("name")), attrgetter("name")
        )
    }
    type_classes = {
        class_.id: class_
        for attr in uml_class.attributes.values()
        if attr.type is not None
        if (class_ := classes_by_name[attr.type])
    }

    return type_classes


def gen_slot_from_attr(
    uml_attr: uml_model.Attribute, uml_project: uml_model.Project
) -> linkml_model.SlotDefinition:
    classes_by_name = {
        name: next(classes)
        for name, classes in groupby(
            sorted(uml_project.classes.values(), key=attrgetter("name")), attrgetter("name")
        )
    }
    domain_class = uml_project.classes[uml_attr.class_]

    range_ = None
    if uml_attr.type is not None:
        type_class = classes_by_name[uml_attr.type]
        if type_class.stereotype == uml_model.ClassStereotype.PRIMITIVE:
            range_ = map_primitive_data_type(uml_attr.type)
        else:
            range_ = convert_camel_to_snake(gen_safe_name(type_class.name))

    return linkml_model.SlotDefinition(
        name=convert_camel_to_snake(gen_safe_name(uml_attr.name)),
        range=range_,
        description=uml_attr.notes,
        required=_slot_required(uml_attr.lower_bound),
        multivalued=_slot_multivalued(uml_attr.lower_bound),
        slot_uri=gen_curie(f"{domain_class.name}.{uml_attr.name}", CIM_PREFIX),
    )


def _slot_required(lower_bound: uml_model.CardinalityValue) -> bool:
    return lower_bound == "*" or lower_bound > 0


def _slot_multivalued(upper_bound: uml_model.CardinalityValue) -> bool:
    return upper_bound == "*" or upper_bound > 1


def gen_slot_from_relation(
    uml_relation: uml_model.Relation, uml_class: uml_model.Class
) -> linkml_model.SlotDefinition:
    classes_by_name = {
        name: next(classes)
        for name, classes in groupby(
            sorted(uml_project.classes.values(), key=attrgetter("name")), attrgetter("name")
        )
    }
    domain_class = uml_project.classes[uml_attr.class_]

    range_ = None
    if uml_attr.type is not None:
        type_class = classes_by_name[uml_attr.type]
        if type_class.stereotype == uml_model.ClassStereotype.PRIMITIVE:
            range_ = map_primitive_data_type(uml_attr.type)
        else:
            range_ = convert_camel_to_snake(gen_safe_name(type_class.name))
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
    uml_class: uml_model.Class, uml_project: uml_model.Project
) -> linkml_model.ClassDefinition:
    super_class = get_super_class(uml_class, uml_project)

    attr_slots = {
        convert_camel_to_snake(gen_safe_name(attr_name)): gen_slot_from_attr(attr, uml_project)
        for attr_name, attr in uml_class.attributes.items()
    }
    # relation_slots = {
    #     convert_camel_to_snake(
    #         gen_safe_name(rel.dest_role or rel.dest_class.name)
    #     ): gen_slot_from_relation(rel, uml_class)
    #     for rel in uml_project.relations.values()
    #     if rel.source_class == uml_class.id
    #     if rel.type != uml_model.RelationType.GENERALIZATION
    # }

    return linkml_model.ClassDefinition(
        name=gen_safe_name(uml_class.name),
        class_uri=gen_curie(uml_class.name, CIM_PREFIX),
        is_a=super_class.name if super_class else None,
        description=uml_class.note,
        attributes=attr_slots,  # | relation_slots,
    )
