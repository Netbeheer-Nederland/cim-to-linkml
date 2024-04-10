from datetime import datetime
from functools import lru_cache
from typing import Optional
from urllib.parse import quote

import cim_to_linkml.linkml_model as linkml_model
import cim_to_linkml.uml_model as uml_model

LINKML_METAMODEL_VERSION = "1.7.0"
GITHUB_BASE_URL = "https://github.com/"
GITHUB_REPO_URL = "https://github.com/bartkl/cim-to-linkml"


def gen_schema_id(uml_package: uml_model.Package, uml_project: uml_model.Project) -> linkml_model.URI:
    """
    Example:
    TC57CIM.IEC61970.Dynamics.StandardModels
        ->
    https://cim.ucaiug.io/ns#TC57CIM.IEC61970.Dynamics.StandardModels
    """

    qname = uml_project.packages.get_qualified_name(uml_package.id)
    return linkml_model.CIM_BASE_URI + qname


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


def gen_curie(name: str, prefix: str) -> str:  # TODO: Implement and move.
    # Also escape characters.
    return f"{prefix}:{quote(name)}"


def _gen_class_with_deps(
    uml_class: uml_model.Class, uml_project: uml_model.Project, results: tuple[dict, dict] | None = None
) -> tuple[dict, dict]:
    """Generates the class dependencies.

    This method does the heavy lifting. It recursively traverses all dependencies
    of the given UML class, e.g. its ancestor classes, associated classes and
    enum types, etc.

    Every class dependency is either a class or enum class, and once generated to LinkML
    elements they are stored in `results`.
    """

    if results is None:
        results = {}, {}

    match uml_class.stereotype:
        case uml_model.ClassStereotype.PRIMITIVE:
            # TODO: Log.
            return results
        case uml_model.ClassStereotype.ENUMERATION:
            enum = gen_enum(uml_class, uml_project)
            results[1][uml_class.name] = enum
        case uml_model.ClassStereotype.CIMDATATYPE:
            class_ = gen_class(uml_class, uml_project)
            results[0][uml_class.name] = class_
        case None | _:
            class_ = gen_class(uml_class, uml_project)
            results[0][uml_class.name] = class_

    uml_dep_classes = tuple()  # TODO: Now duplicates can be stored. Improve this.

    uml_super_class = get_super_class(uml_class, uml_project)
    if uml_super_class:
        uml_dep_classes = uml_dep_classes + (uml_super_class,)

    uml_dep_classes = (
        uml_dep_classes + get_attr_type_classes(uml_class, uml_project) + get_rel_type_classes(uml_class, uml_project)
    )

    for uml_dep_class in uml_dep_classes:
        if uml_dep_class.name in results[0]:
            continue
        results = _gen_class_with_deps(uml_dep_class, uml_project, results)
    return results


def gen_schema_for_package(
    uml_package_id: uml_model.ObjectID, uml_classes: list[uml_model.Class], uml_project: uml_model.Project
) -> linkml_model.Schema:
    uml_package = uml_project.packages.by_id[uml_package_id]

    # (Re-)initialize generator state.
    classes: dict[linkml_model.ClassName, linkml_model.Class] = {}
    enums: dict[linkml_model.EnumName, linkml_model.Enum] = {}

    for uml_class in uml_classes:
        results = _gen_class_with_deps(uml_class, uml_project)
        classes.update(results[0])
        enums.update(results[1])

    schema = linkml_model.Schema(
        id=gen_schema_id(uml_package, uml_project),
        name=uml_project.packages.get_qualified_name(uml_package_id),
        title=uml_package.name,
        description=uml_package.notes,
        contributors=["github:bartkl"],
        created_by=GITHUB_REPO_URL,
        generation_date=datetime.now(),
        license="https://www.apache.org/licenses/LICENSE-2.0.txt",
        metamodel_version=LINKML_METAMODEL_VERSION,
        imports=["linkml:types"],
        prefixes={
            "linkml": "https://w3id.org/linkml/",
            "github": "https://github.com/",
            linkml_model.CIM_PREFIX: linkml_model.CIM_BASE_URI,
        },
        default_curi_maps=["semweb_context"],
        default_prefix=linkml_model.CIM_PREFIX,
        default_range="string",
        classes=classes,
        enums=enums,
    )

    return schema


@lru_cache(maxsize=1942)
def gen_enum(uml_enum: uml_model.Class, uml_project: uml_model.Project) -> linkml_model.Enum:
    assert uml_enum.stereotype == uml_model.ClassStereotype.ENUMERATION
    package = uml_project.packages.by_id[uml_enum.package]

    return linkml_model.Enum(
        name=uml_enum.name,
        enum_uri=gen_curie(uml_enum.name, linkml_model.CIM_PREFIX),
        description=uml_enum.note,
        permissible_values={
            uml_enum_val.name: linkml_model.PermissibleValue(
                meaning=gen_curie(f"{uml_enum.name}.{uml_enum_val.name}", linkml_model.CIM_PREFIX)
            )._asdict()
            for uml_enum_val in uml_enum.attributes
        },
        from_schema=gen_schema_id(package, uml_project),
    )


@lru_cache(maxsize=1947)
def get_super_class(uml_class: uml_model.Class, uml_project: uml_model.Project) -> Optional[uml_model.Class]:
    rels = uml_project.relations.by_source_class.get(uml_class.id, [])
    for uml_relation in rels:
        if uml_relation.type != uml_model.RelationType.GENERALIZATION:
            continue

        try:
            source_class = uml_project.classes.by_id[uml_relation.source_class]
        except KeyError as e:
            continue  # Bad data, but no superclass for sure.

        if source_class.id == uml_class.id:
            super_class = uml_project.classes.by_id[uml_relation.dest_class]
            return super_class
    return None


@lru_cache(maxsize=1942)
def get_attr_type_classes(uml_class: uml_model.Class, uml_project: uml_model.Project) -> tuple[uml_model.Class]:
    type_classes = tuple(
        class_
        for attr in uml_class.attributes
        if attr.type is not None
        if (class_ := uml_project.classes.by_name[attr.type])
    )

    return type_classes


@lru_cache(maxsize=1942)
def get_rel_type_classes(uml_class: uml_model.Class, uml_project: uml_model.Project) -> tuple[uml_model.Class]:
    from_classes = tuple()
    to_classes = tuple()

    for rel in uml_project.relations.by_id.values():
        if rel.type == uml_model.RelationType.GENERALIZATION:
            continue
        match uml_class.id:
            case rel.source_class:
                dest_class = uml_project.classes.by_id[rel.dest_class]
                to_classes = to_classes + (dest_class,)
            case rel.dest_class:
                source_class = uml_project.classes.by_id[rel.source_class]
                from_classes = from_classes + (source_class,)

    return from_classes + to_classes


def gen_slot_from_attr(
    uml_attr: uml_model.Attribute, uml_class: uml_model.Class, uml_project: uml_model.Project
) -> linkml_model.Slot:
    type_class = uml_project.classes.by_name[uml_attr.type]
    if type_class.stereotype == uml_model.ClassStereotype.PRIMITIVE:
        range_ = map_primitive_data_type(uml_attr.type)
    else:
        range_ = type_class.name

    return linkml_model.Slot(
        name=uml_attr.name,
        range=range_,
        description=uml_attr.notes,
        required=_slot_required(uml_attr.lower_bound),
        multivalued=_slot_multivalued(uml_attr.lower_bound),
        slot_uri=gen_curie(f"{uml_class.name}.{uml_attr.name}", linkml_model.CIM_PREFIX),
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
                name=uml_relation.dest_role or dest_class.name,
                range=dest_class.name,
                description=uml_relation.dest_role_note,
                required=_slot_required(uml_relation.dest_card.lower_bound),
                multivalued=_slot_multivalued(uml_relation.dest_card.upper_bound),
                slot_uri=gen_curie(
                    f"{source_class.name}.{uml_relation.dest_role or dest_class.name}",
                    linkml_model.CIM_PREFIX,
                ),
            )
        case "dest->source":
            return linkml_model.Slot(
                name=uml_relation.source_role or source_class.name,
                range=source_class.name,
                description=uml_relation.source_role_note,
                required=_slot_required(uml_relation.source_card.lower_bound),
                multivalued=_slot_multivalued(uml_relation.source_card.upper_bound),
                slot_uri=gen_curie(
                    f"{dest_class.name}.{uml_relation.source_role or source_class.name}",
                    linkml_model.CIM_PREFIX,
                ),
            )
        case _:
            raise TypeError(f"Provided direction value was invalid. (relation ID: {uml_relation.id})")


@lru_cache(maxsize=1942)
def gen_class(uml_class: uml_model.Class, uml_project: uml_model.Project) -> linkml_model.Class:
    super_class = get_super_class(uml_class, uml_project)
    package = uml_project.packages.by_id[uml_class.package]

    attr_slots = tuple(
        slot for uml_attr in uml_class.attributes if (slot := gen_slot_from_attr(uml_attr, uml_class, uml_project))
    )

    from_relation_slots = tuple(
        slot
        for rel in uml_project.relations.by_source_class.get(uml_class.id, [])
        if rel and rel.type != uml_model.RelationType.GENERALIZATION
        if (slot := gen_slot_from_relation(rel, uml_project, "source->dest"))
    )

    to_relation_slots = tuple(
        slot
        for rel in uml_project.relations.by_dest_class.get(uml_class.id, [])
        if rel and rel.type != uml_model.RelationType.GENERALIZATION
        if (slot := gen_slot_from_relation(rel, uml_project, "dest->source"))
    )

    annotations = {}
    if uml_class.stereotype == uml_model.ClassStereotype.CIMDATATYPE:
        annotations["represents_cim_data_type"] = True

    class_ = linkml_model.Class(
        name=uml_class.name,
        class_uri=gen_curie(uml_class.name, linkml_model.CIM_PREFIX),
        is_a=super_class.name if super_class else None,
        annotations=annotations,
        description=uml_class.note,
        attributes={slot.name: slot for slot in (attr_slots + from_relation_slots + to_relation_slots)} or None,
        from_schema=gen_schema_id(package, uml_project),
    )

    return class_
