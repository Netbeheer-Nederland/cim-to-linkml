from datetime import datetime

from cim_to_linkml.cim18.linkml.class_.generate import generate_class
from cim_to_linkml.cim18.linkml.enumeration.generate import generate_enumeration
from cim_to_linkml.cim18.linkml.model import CIM_PREFIX, CIM_BASE_URI, CIM_MODEL_LICENSE
from cim_to_linkml.cim18.linkml.schema.model import GITHUB_REPO_URL, GITHUB_BASE_URL, LINKML_METAMODEL_VERSION, \
    SCHEMA_ID, SCHEMA_NAME
from cim_to_linkml.cim18.linkml.schema.model import Schema as LinkMLSchema
from cim_to_linkml.cim18.linkml.type_.generate import generate_type
from cim_to_linkml.cim18.uml.class_.model import ClassStereotype
from cim_to_linkml.cim18.uml.model import ObjectID as UMLObjectID
from cim_to_linkml.cim18.uml.project.model import Project as UMLProject


def generate_schema(uml_project: UMLProject, root_package_id: UMLObjectID) -> LinkMLSchema:
    uml_root_package = uml_project.packages[root_package_id]

    classes, slots, enums, types = {}, {}, {}, {}

    for uml_class in uml_project.classes.values():
        match uml_class.stereotype:
            case ClassStereotype.PRIMITIVE:
                continue
            case ClassStereotype.ENUMERATION:
                continue  # TODO: Remove.
                enums[uml_class.name] = generate_enumeration(uml_class)
            case ClassStereotype.CIMDATATYPE:
                continue  # TODO: Remove.
                types[uml_class.name] = generate_type(uml_class)
            case None | _:
                classes[uml_class.name] = generate_class(uml_class)

    # inline()

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
        classes=classes,
        slots=slots,
        enums=enums,
        types=types,
    )

    return schema
