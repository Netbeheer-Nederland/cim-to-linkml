from datetime import datetime

from cim_to_linkml.cim18.linkml.class_.generate import generate_class, add_slots
from cim_to_linkml.cim18.linkml.class_.model import Class as LinkMLClass
from cim_to_linkml.cim18.linkml.enumeration.generate import generate_enumeration
from cim_to_linkml.cim18.linkml.enumeration.model import Enum as LinkMLEnum
from cim_to_linkml.cim18.linkml.model import CIM_PREFIX, CIM_BASE_URI, CIM_MODEL_LICENSE, SlotName, EnumName, TypeName
from cim_to_linkml.cim18.linkml.schema.model import GITHUB_REPO_URL, GITHUB_BASE_URL, LINKML_METAMODEL_VERSION, \
    SCHEMA_ID, SCHEMA_NAME
from cim_to_linkml.cim18.linkml.schema.model import Schema as LinkMLSchema
from cim_to_linkml.cim18.linkml.slot.generate import generate_relation_slots
from cim_to_linkml.cim18.linkml.slot.model import Slot as LinkMLSlot
from cim_to_linkml.cim18.linkml.type_.generate import generate_cim_datatype
from cim_to_linkml.cim18.linkml.type_.model import Type as LinkMLType
from cim_to_linkml.cim18.uml.class_.model import ClassStereotype, ClassName
from cim_to_linkml.cim18.uml.model import TOP_LEVEL_PACKAGE_ID
from cim_to_linkml.cim18.uml.package.model import PackageStatus
from cim_to_linkml.cim18.uml.project.model import Project as UMLProject
from cim_to_linkml.cim18.uml.relation.model import Relation as UMLRelation, RelationType


def _is_uml_relation_between_normative_classes(uml_relation: UMLRelation, uml_project: UMLProject) -> bool:
    try:
        source_class = uml_project.classes[uml_relation.source_class]
        source_class_package = uml_project.packages[source_class.package]
        dest_class = uml_project.classes[uml_relation.dest_class]
        dest_class_package = uml_project.packages[dest_class.package]
    except KeyError:
        return False  # Assumption: if not found, the classes are already filtered.

    return (source_class_package.status == PackageStatus.NORMATIVE and
            dest_class_package.status == PackageStatus.NORMATIVE)


def generate_schema(uml_project: UMLProject, only_normative: bool = True) -> LinkMLSchema:
    uml_root_package = uml_project.packages[TOP_LEVEL_PACKAGE_ID]

    linkml_classes: dict[ClassName, LinkMLClass] = {}
    linkml_slots: dict[SlotName, LinkMLSlot] = {}
    linkml_enums: dict[EnumName, LinkMLEnum] = {}
    linkml_types: dict[TypeName, LinkMLType] = {}

    # UML Classes.
    for uml_class in uml_project.classes.values():
        uml_class_package = uml_project.packages[uml_class.package]
        if only_normative and uml_class_package.status != PackageStatus.NORMATIVE:
            continue

        match uml_class.stereotype:
            case ClassStereotype.PRIMITIVE:
                continue
            case ClassStereotype.ENUMERATION:
                linkml_enums[uml_class.name] = generate_enumeration(uml_class, uml_project)
            case ClassStereotype.CIM_DATATYPE:
                linkml_types[uml_class.name] = generate_cim_datatype(uml_class, uml_project)
            case ClassStereotype.COMPOUND:
                ...
            case None | _:
                linkml_classes[uml_class.name] = generate_class(uml_class, uml_project)

    # UML Relations.
    for uml_relation in uml_project.relations.values():
        if only_normative and not _is_uml_relation_between_normative_classes(uml_relation, uml_project):
            continue

        match uml_relation.type:
            case RelationType.ASSOCIATION:
                source_slot, dest_slot = generate_relation_slots(uml_relation, uml_project)
                linkml_slots[source_slot._name] = source_slot
                linkml_slots[dest_slot._name] = dest_slot
            case RelationType.GENERALIZATION | RelationType.AGGREGATION:
                source_class = uml_project.classes[uml_relation.source_class]
                dest_class = uml_project.classes[uml_relation.dest_class]
                linkml_classes[source_class.name].is_a = dest_class.name

    add_slots(linkml_classes, linkml_slots)

    schema = LinkMLSchema(
        id=SCHEMA_ID,
        name=SCHEMA_NAME,
        title=uml_root_package.name,
        description=uml_root_package.notes,
        contributors=["github:bartkl"],
        created_by=GITHUB_REPO_URL,
        generation_date=datetime.now(),
        license=CIM_MODEL_LICENSE,
        metamodel_version=LINKML_METAMODEL_VERSION,
        imports=["linkml:types"],
        prefixes={
            "linkml": "https://w3id.org/linkml/",
            "github": GITHUB_BASE_URL,
            CIM_PREFIX: CIM_BASE_URI,
        },
        default_curi_maps=["semweb_context"],
        default_prefix=CIM_PREFIX,
        default_range="string",
        classes=linkml_classes,
        slots=linkml_slots,
        enums=linkml_enums,
        types=linkml_types,
    )

    return schema
