from datetime import datetime

from cim_to_linkml.cim18.linkml.class_.generate import generate_class
from cim_to_linkml.cim18.linkml.class_.model import Class as LinkMLClass
from cim_to_linkml.cim18.linkml.class_.model import ClassName as LinkMLClassName
from cim_to_linkml.cim18.linkml.enumeration.model import Enum as LinkMLEnum
from cim_to_linkml.cim18.linkml.enumeration.model import EnumName as LinkMLEnumName
from cim_to_linkml.cim18.linkml.model import CIM_PREFIX, CIM_BASE_URI, CIM_MODEL_LICENSE
from cim_to_linkml.cim18.linkml.schema.model import GITHUB_REPO_URL, GITHUB_BASE_URL, LINKML_METAMODEL_VERSION, \
    SCHEMA_ID, SCHEMA_NAME
from cim_to_linkml.cim18.linkml.schema.model import Schema as LinkMLSchema
from cim_to_linkml.cim18.uml.model import ObjectID as UMLObjectID
from cim_to_linkml.cim18.uml.project.model import Project as UMLProject


def _generate_classes(uml_project: UMLProject) -> dict[LinkMLClassName, LinkMLClass]:
    return {class_.name: generate_class(class_) for class_ in uml_project.classes.values()}


# def _generate_enums(uml_project: UMLProject) -> dict[LinkMLEnumName, LinkMLEnum]:
#     return {enum.name: generate_enum(enum) for enum in uml_project.classes.values()}


def generate_schema(uml_project: UMLProject, root_package_id: UMLObjectID) -> LinkMLSchema:
    uml_root_package = uml_project.packages[root_package_id]

    classes = {}
    enums = {}

    # for uml_class in uml_project.classes.values():
    #     _classes, _enums = _generate_elements_for_class(uml_class, uml_project)
    #     classes.update(_classes)
    #     enums.update(_enums)

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
        classes=_generate_classes(uml_project),
        # enums=_generate_enums(uml_project),
    )

    return schema
