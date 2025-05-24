from datetime import datetime

from cim_to_linkml.cim18.linkml.class_.generate import generate_class
from cim_to_linkml.cim18.linkml.enumeration.generate import generate_enumeration
from cim_to_linkml.cim18.linkml.model import CIM_PREFIX, CIM_BASE_URI, CIM_MODEL_LICENSE
from cim_to_linkml.cim18.linkml.schema.model import GITHUB_REPO_URL, GITHUB_BASE_URL, LINKML_METAMODEL_VERSION, \
    SCHEMA_ID, SCHEMA_NAME
from cim_to_linkml.cim18.linkml.schema.model import Schema as LinkMLSchema
from cim_to_linkml.cim18.linkml.type_.generate import generate_cim_datatype
from cim_to_linkml.cim18.uml.class_.model import ClassStereotype
from cim_to_linkml.cim18.uml.model import TOP_LEVEL_PACKAGE_ID
from cim_to_linkml.cim18.uml.package.model import PackageStatus
from cim_to_linkml.cim18.uml.project.model import Project as UMLProject
from cim_to_linkml.uml_model import Relation as UMLRelation


def _is_uml_relation_between_normative_classes(uml_relation: UMLRelation, uml_project: UMLProject) -> bool:
    source_class = uml_project.classes[uml_relation.source_class]
    source_class_package = uml_project.packages[source_class.package]

    dest_class = uml_project.classes[uml_relation.dest_class]
    dest_class_package = uml_project.packages[dest_class.package]

    return (source_class_package.status == PackageStatus.NORMATIVE and
            dest_class_package.status == PackageStatus.NORMATIVE)


def generate_schema(uml_project: UMLProject, only_normative: bool = True) -> LinkMLSchema:
    uml_root_package = uml_project.packages[TOP_LEVEL_PACKAGE_ID]

    linkml_classes, linkml_slots, linkml_enums, linkml_types = {}, {}, {}, {}

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

    for uml_relation in uml_project.relations.values():
        if only_normative and not _is_uml_relation_between_normative_classes(uml_relation, uml_project):
            continue

        ...

    # assemble() / inline()

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
        default_curie_maps=["semweb_context"],
        default_prefix=CIM_PREFIX,
        default_range="string",
        classes=linkml_classes,
        slots=linkml_slots,
        enums=linkml_enums,
        types=linkml_types,
    )

    return schema
