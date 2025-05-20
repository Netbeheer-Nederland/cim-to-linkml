from datetime import datetime

from cim_to_linkml.cim18.linkml.model import CIM_PREFIX, CIM_BASE_URI
from cim_to_linkml.cim18.linkml.schema.model import GITHUB_REPO_URL, LINKML_METAMODEL_VERSION, SCHEMA_ID, SCHEMA_NAME
from cim_to_linkml.cim18.linkml.schema.model import Schema as LinkMLSchema
from cim_to_linkml.cim18.uml.model import ObjectID as UMLObjectID
from cim_to_linkml.cim18.uml.project.model import Project as UMLProject


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
        license="https://www.apache.org/licenses/LICENSE-2.0.txt",
        metamodel_version=LINKML_METAMODEL_VERSION,
        imports=["linkml:types"],
        prefixes={
            "linkml": "https://w3id.org/linkml/",
            "github": "https://github.com/",
            CIM_PREFIX: CIM_BASE_URI,
        },
        default_curi_maps=["semweb_context"],
        default_prefix=CIM_PREFIX,
        default_range="string",
        classes=classes,
        enums=enums,
    )

    return schema
